import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile, BadZipFile

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DIR = BASE_DIR / "ai" / "data" / "raw" / "senatran"

SOURCE_PAGE = (
    "https://www.gov.br/transportes/pt-br/assuntos/transito/"
    "conteudo-Senatran/frota-de-veiculos-2026"
)

CKAN_PACKAGE_API = (
    "https://dados.transportes.gov.br/api/3/action/package_show"
    "?id=registro-nacional-de-veiculos-automotores-renavam"
)

CHUNK_SIZE = 8 * 1024 * 1024


def sha256_file(file_path):
    digest = hashlib.sha256()

    with file_path.open("rb") as stream:
        for chunk in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def fetch_json(url):
    request = Request(
        url,
        headers={
            "User-Agent": "GerenciamentoDeVeiculos/1.0",
        },
    )

    with urlopen(request, timeout=60) as response:
        return json.load(response)


def find_resource(month):
    payload = fetch_json(CKAN_PACKAGE_API)

    resources = payload.get("result", {}).get("resources", [])

    if not resources:
        raise RuntimeError(
            "Nenhum recurso encontrado no dataset RENAVAM."
        )

    target_date = datetime.strptime(
        month,
        "%Y-%m",
    )

    month_names = {
        1: ("janeiro", "jan"),
        2: ("fevereiro", "fev"),
        3: ("março", "marco", "mar"),
        4: ("abril", "abr"),
        5: ("maio", "mai"),
        6: ("junho", "jun"),
        7: ("julho", "jul"),
        8: ("agosto", "ago"),
        9: ("setembro", "set"),
        10: ("outubro", "out"),
        11: ("novembro", "nov"),
        12: ("dezembro", "dez"),
    }

    names = month_names[target_date.month]
    year = str(target_date.year)

    candidates = []

    for resource in resources:

        text = " ".join(
            str(resource.get(field, ""))
            for field in (
                "name",
                "description",
                "url",
                "format",
            )
        ).lower()

        if year not in text:
            continue

        if not any(name in text for name in names):
            continue

        if "marca" not in text:
            continue

        if "modelo" not in text:
            continue

        if not resource.get("url"):
            continue

        candidates.append(resource)

    if not candidates:
        raise RuntimeError(
            f"Nenhum recurso marca/modelo encontrado para {month}."
        )

    return candidates[0]


def get_remote_size(url):
    request = Request(
        url,
        headers={
            "User-Agent": "GerenciamentoDeVeiculos/1.0",
            "Range": "bytes=0-0",
        },
    )

    with urlopen(request, timeout=60) as response:

        content_range = response.headers.get(
            "Content-Range"
        )

        if content_range:

            match = re.search(
                r"/(\d+)$",
                content_range,
            )

            if match:
                return int(match.group(1))

        content_length = response.headers.get(
            "Content-Length"
        )

        if content_length:
            return int(content_length)

    raise RuntimeError(
        "Servidor não informou o tamanho do arquivo."
    )


def download_resumable(url, destination, expected_size):

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    current_size = (
        destination.stat().st_size
        if destination.exists()
        else 0
    )

    if current_size > expected_size:

        destination.unlink()
        current_size = 0

    mode = "ab" if current_size else "wb"

    print(
        f"Tamanho remoto: {expected_size:,} bytes"
    )

    print(
        f"Já baixado:     {current_size:,} bytes"
    )

    with destination.open(mode) as output:

        while current_size < expected_size:

            end = min(
                current_size + CHUNK_SIZE - 1,
                expected_size - 1,
            )

            request = Request(
                url,
                headers={
                    "User-Agent":
                        "GerenciamentoDeVeiculos/1.0",
                    "Range":
                        f"bytes={current_size}-{end}",
                },
            )

            with urlopen(
                request,
                timeout=300,
            ) as response:

                status = response.status

                if status != 206:

                    raise RuntimeError(
                        "Servidor não retornou HTTP 206 "
                        f"para Range. Status: {status}"
                    )

                while current_size <= end:

                    chunk = response.read(
                        min(
                            1024 * 1024,
                            end - current_size + 1,
                        )
                    )

                    if not chunk:
                        break

                    output.write(chunk)
                    current_size += len(chunk)

                    print(
                        f"\rDownload: "
                        f"{current_size:,}/"
                        f"{expected_size:,} bytes "
                        f"({current_size / expected_size:.1%})",
                        end="",
                        flush=True,
                    )

            if current_size <= end:
                raise RuntimeError(
                    "Conexão interrompida antes "
                    "do fim do chunk."
                )

    print()

    if destination.stat().st_size != expected_size:

        raise RuntimeError(
            "Download incompleto: "
            f"{destination.stat().st_size:,}/"
            f"{expected_size:,} bytes"
        )


def validate_zip(file_path):

    if not file_path.exists():
        raise RuntimeError(
            f"Arquivo não encontrado: {file_path}"
        )

    try:

        with ZipFile(file_path) as archive:

            bad_file = archive.testzip()

            if bad_file:

                raise RuntimeError(
                    f"ZIP corrompido. Primeiro arquivo "
                    f"com erro: {bad_file}"
                )

            files = archive.namelist()

            if not files:

                raise RuntimeError(
                    "ZIP vazio."
                )

            print(
                f"ZIP válido: {len(files)} arquivo(s)"
            )

            for name in files:
                print(f"  {name}")

    except BadZipFile as exc:

        raise RuntimeError(
            "Arquivo baixado não é um ZIP válido "
            "ou está incompleto."
        ) from exc


def main():

    parser = argparse.ArgumentParser(
        description="Download SENATRAN RENAVAM"
    )

    parser.add_argument(
        "--month",
        default="2026-07",
        help="Mês no formato YYYY-MM",
    )

    args = parser.parse_args()

    if not re.fullmatch(
        r"\d{4}-\d{2}",
        args.month,
    ):
        raise SystemExit(
            "--month deve estar no formato YYYY-MM"
        )

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"Buscando SENATRAN RENAVAM: {args.month}"
    )

    resource = find_resource(args.month)

    url = resource["url"]

    destination = (
        RAW_DIR
        / f"renavam_{args.month}.zip"
    )

    print(
        f"Recurso: {resource.get('name')}"
    )

    print(
        f"URL: {url}"
    )

    expected_size = get_remote_size(url)

    download_resumable(
        url,
        destination,
        expected_size,
    )

    print("\nValidando ZIP...")

    validate_zip(destination)

    actual_size = destination.stat().st_size
    actual_hash = sha256_file(destination)

    manifest = {
        "source": "SENATRAN",
        "dataset": "RENAVAM",
        "resource_id": resource.get("id"),
        "resource_name": resource.get("name"),
        "source_url": url,
        "source_page": SOURCE_PAGE,
        "downloaded_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "file": destination.name,
        "size_bytes": actual_size,
        "remote_size_bytes": expected_size,
        "sha256": actual_hash,
        "validated": True,
    }

    manifest_path = (
        RAW_DIR
        / f"renavam_{args.month}.manifest.json"
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("DOWNLOAD CONCLUÍDO E VALIDADO")
    print(f"Arquivo: {destination.name}")
    print(f"Tamanho: {actual_size:,} bytes")
    print(f"SHA-256: {actual_hash}")
    print(f"Manifesto: {manifest_path}")


if __name__ == "__main__":

    try:
        main()

    except Exception as exc:

        print(
            f"ERRO: {exc}",
            file=sys.stderr,
        )

        raise SystemExit(1)
