from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "senatran"
    / "senatran_classificado_2026-07.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed" / "senatran"


def load_data():
    return pd.read_csv(INPUT_PATH)


def build_municipality_summary(u):
    v = (
        u.groupby(
            ["state", "municipality", "vehicle_class"]
        )["vehicle_count"]
        .sum()
        .unstack(fill_value=0)
    )

    return v.reset_index()


def normalize_columns(u):
    expected_columns = [
        "CARRO",
        "MOTO",
        "PESADO",
        "IMPLEMENTO",
        "NAO_CLASSIFICADO",
        "OUTRO",
    ]

    for v in expected_columns:
        if v not in u.columns:
            u[v] = 0

    u["total_fleet"] = u[expected_columns].sum(axis=1)

    return u[
        [
            "state",
            "municipality",
            "total_fleet",
            "CARRO",
            "MOTO",
            "PESADO",
            "IMPLEMENTO",
            "NAO_CLASSIFICADO",
            "OUTRO",
        ]
    ]


def validate_total(u):
    x = u["total_fleet"].sum()

    print("\n=== VALIDAÇÃO DO TOTAL ===")
    print(f"Total agregado: {x:,}")

    expected = 135_374_097

    if x != expected:
        raise ValueError(
            f"Total inconsistente: {x:,} != {expected:,}"
        )

    print("Total validado.")


def validate_duplicates(u):
    x = u.duplicated(
        subset=["state", "municipality"]
    ).sum()

    print("\n=== DUPLICIDADES ===")
    print(f"Duplicidades UF + município: {x}")

    if x != 0:
        raise ValueError(
            "Existem duplicidades em UF + município."
        )


def save_data(u):
    output_path = (
        OUTPUT_DIR
        / "senatran_municipio_2026-07.csv"
    )

    u.to_csv(output_path, index=False)

    print(f"\nArquivo gerado: {output_path}")


def main():
    print("Carregando SENATRAN classificado...")

    u = load_data()

    print(f"Registros: {len(u):,}")

    v = build_municipality_summary(u)

    v = normalize_columns(v)

    validate_total(v)

    validate_duplicates(v)

    print("\n=== RESUMO ===")
    print(f"Municípios: {len(v):,}")

    print("\n=== AMOSTRA ===")
    print(v.head(20).to_string(index=False))

    save_data(v)


if __name__ == "__main__":
    main()
