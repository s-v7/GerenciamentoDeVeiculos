import argparse
import hashlib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DIR = (
    BASE_DIR
    / "ai"
    / "data"
    / "raw"
    / "senatran"
)


def sha256_file(file_path):

    digest = hashlib.sha256()

    with file_path.open("rb") as stream:

        for chunk in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def main():

    parser = argparse.ArgumentParser(
        description="Valida dados SENATRAN"
    )

    parser.add_argument(
        "--month",
        default="2026-07",
    )

    args = parser.parse_args()

    manifest_path = (
        RAW_DIR
        / f"renavam_{args.month}.manifest.json"
    )

    if not manifest_path.exists():

        raise SystemExit(
            f"Manifesto não encontrado: "
            f"{manifest_path}"
        )

    manifest = json.loads(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    file_path = (
        RAW_DIR
        / manifest["file"]
    )

    if not file_path.exists():

        raise SystemExit(
            f"Arquivo não encontrado: "
            f"{file_path}"
        )

    actual_hash = sha256_file(
        file_path
    )

    expected_hash = manifest["sha256"]

    if actual_hash != expected_hash:

        raise SystemExit(
            "CHECKSUM INVÁLIDO\n"
            f"Esperado: {expected_hash}\n"
            f"Atual:    {actual_hash}"
        )

    actual_size = (
        file_path.stat().st_size
    )

    expected_size = manifest[
        "size_bytes"
    ]

    if actual_size != expected_size:

        raise SystemExit(
            "TAMANHO INVÁLIDO\n"
            f"Esperado: {expected_size}\n"
            f"Atual:    {actual_size}"
        )

    print(
        "OK: arquivo SENATRAN validado"
    )

    print(
        f"Arquivo: {file_path.name}"
    )

    print(
        f"Tamanho: {actual_size} bytes"
    )

    print(
        f"SHA-256: {actual_hash}"
    )


if __name__ == "__main__":
    main()
