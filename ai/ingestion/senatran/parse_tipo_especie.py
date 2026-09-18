import argparse
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[3]

RAW_DIR = BASE_DIR / "ai" / "data" / "raw" / "senatran"
PROCESSED_DIR = BASE_DIR / "ai" / "data" / "processed" / "senatran"


INPUT_NAME = "tipo_especie_eixos_2026-07.xlsx"


OUTPUT_COLUMNS = [
    "state",
    "municipality",
    "vehicle_type",
    "vehicle_species",
    "axles",
    "vehicle_count",
]


def normalize_text(value):
    if pd.isna(value):
        return ""

    return " ".join(
        str(value).strip().split()
    )


def parse_file(input_path, output_path):

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    source = pd.read_excel(
        input_path,
        sheet_name="Layout G",
    )

    source.columns = [
        normalize_text(column)
        for column in source.columns
    ]

    source = source.rename(
        columns={
            "UF": "state",
            "Município": "municipality",
            "Tipo Veículo": "vehicle_type",
            "Espécie Veículo": "vehicle_species",
            "Eixos": "axles",
            "Qtd. Veículos": "vehicle_count",
        }
    )

    for column in [
        "state",
        "municipality",
        "vehicle_type",
        "vehicle_species",
    ]:
        source[column] = source[column].map(
            normalize_text
        )

    source["axles"] = pd.to_numeric(
        source["axles"],
        errors="coerce",
    )

    source["vehicle_count"] = pd.to_numeric(
        source["vehicle_count"],
        errors="coerce",
    )

    invalid = (
        (source["state"] == "")
        | (source["municipality"] == "")
        | (source["vehicle_type"] == "")
        | (source["vehicle_species"] == "")
        | source["axles"].isna()
        | source["vehicle_count"].isna()
        | (source["vehicle_count"] <= 0)
    )

    invalid_rows = int(invalid.sum())

    source = source.loc[
        ~invalid,
        OUTPUT_COLUMNS,
    ].copy()

    source["axles"] = source["axles"].astype(
        "int64"
    )

    source["vehicle_count"] = source[
        "vehicle_count"
    ].astype("int64")

    source.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )

    return {
        "total_rows": int(len(source) + invalid_rows),
        "invalid_rows": invalid_rows,
        "valid_rows": int(len(source)),
        "total_vehicles": int(
            source["vehicle_count"].sum()
        ),
    }


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Parse SENATRAN Tipo/Espécie/Eixos"
        )
    )

    parser.add_argument(
        "--month",
        default="2026-07",
    )

    args = parser.parse_args()

    input_path = (
        RAW_DIR
        / INPUT_NAME
    )

    output_path = (
        PROCESSED_DIR
        / (
            f"senatran_tipo_especie_eixos_"
            f"{args.month}.csv"
        )
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
    print("Resultado:")
    print(
        f"Total de registros: "
        f"{result['total_rows']:,}"
    )
    print(
        f"Registros válidos: "
        f"{result['valid_rows']:,}"
    )
    print(
        f"Registros inválidos: "
        f"{result['invalid_rows']:,}"
    )
    print(
        f"Total de veículos: "
        f"{result['total_vehicles']:,}"
    )


if __name__ == "__main__":
    main()
