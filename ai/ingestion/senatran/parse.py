import argparse
import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DIR = BASE_DIR / "ai" / "data" / "raw" / "senatran"
PROCESSED_DIR = BASE_DIR / "ai" / "data" / "processed" / "senatran"


INPUT_NAME = (
    "I_Frota_por_UF_Municipio_Marca_e_Modelo_Ano_Julho_2026.TXT"
)


OUTPUT_COLUMNS = [
    "state",
    "municipality",
    "make",
    "model",
    "manufacture_year",
    "vehicle_count",
]


def normalize_text(value):
    return re.sub(
        r"\s+",
        " ",
        value.strip(),
    )


def split_make_model(value):
    value = normalize_text(value)

    if "/" not in value:
        return value, ""

    make, model = value.split(
        "/",
        1,
    )

    return (
        normalize_text(make),
        normalize_text(model),
    )


def normalize_make(make):
    aliases = {
        "CHEV": "CHEVROLET",
        "VW": "VOLKSWAGEN",
        "VOLKSW": "VOLKSWAGEN",
        "FIAT": "FIAT",
        "TOYOTA": "TOYOTA",
        "HONDA": "HONDA",
        "FORD": "FORD",
        "BMW": "BMW",
        "HYUNDAI": "HYUNDAI",
    }

    normalized = make.upper()

    return aliases.get(
        normalized,
        normalized,
    )


def parse_year(value):
    value = value.strip()

    if not value:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def parse_quantity(value):
    value = value.strip()

    if not value:
        return 0

    value = value.replace(
        ".0",
        "",
    )

    return int(value)


def parse_file(input_path, output_path):

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    total_rows = 0
    invalid_rows = 0
    total_vehicles = 0

    with (
        input_path.open(
            "r",
            encoding="utf-8",
            newline="",
        ) as source,
        output_path.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as target,
    ):

        reader = csv.DictReader(
            source,
            delimiter=";",
        )

        writer = csv.DictWriter(
            target,
            fieldnames=OUTPUT_COLUMNS,
        )

        writer.writeheader()

        for row in reader:

            total_rows += 1

            try:

                state = normalize_text(
                    row["UF"]
                )

                municipality = normalize_text(
                    row["Município"]
                )

                make_raw, model = split_make_model(
                    row["Marca Modelo"]
                )

                make = normalize_make(
                    make_raw
                )

                year = parse_year(
                    row[
                        "Ano Fabricação Veículo CRV"
                    ]
                )

                quantity = parse_quantity(
                    row["Qtd. Veículos"]
                )

                if (
                    not state
                    or not municipality
                    or not make
                    or not model
                    or year is None
                    or quantity <= 0
                ):
                    invalid_rows += 1
                    continue

                writer.writerow(
                    {
                        "state": state,
                        "municipality": municipality,
                        "make": make,
                        "model": model,
                        "manufacture_year": year,
                        "vehicle_count": quantity,
                    }
                )

                total_vehicles += quantity

            except (
                KeyError,
                ValueError,
                TypeError,
            ):
                invalid_rows += 1

            if total_rows % 500_000 == 0:

                print(
                    f"Processadas: "
                    f"{total_rows:,} | "
                    f"válidas: "
                    f"{total_rows - invalid_rows:,} | "
                    f"inválidas: "
                    f"{invalid_rows:,}"
                )

    return {
        "total_rows": total_rows,
        "invalid_rows": invalid_rows,
        "valid_rows": total_rows - invalid_rows,
        "total_vehicles": total_vehicles,
    }


def main():

    parser = argparse.ArgumentParser(
        description="Parse SENATRAN RENAVAM"
    )

    parser.add_argument(
        "--month",
        default="2026-07",
    )

    args = parser.parse_args()

    input_path = (
        RAW_DIR
        / "extracted"
        / INPUT_NAME
    )

    output_path = (
        PROCESSED_DIR
        / f"senatran_{args.month}.csv"
    )

    if not input_path.exists():

        raise SystemExit(
            f"Arquivo não encontrado:\n"
            f"{input_path}"
        )

    print(
        f"Entrada: {input_path}"
    )

    print(
        f"Saída:   {output_path}"
    )

    print()
    print("Processando...")

    result = parse_file(
        input_path,
        output_path,
    )

    print()
    print("=== PARSE CONCLUÍDO ===")

    for key, value in result.items():

        print(
            f"{key}: {value:,}"
        )

    print()
    print(
        f"Arquivo gerado: {output_path}"
    )


if __name__ == "__main__":
    main()
