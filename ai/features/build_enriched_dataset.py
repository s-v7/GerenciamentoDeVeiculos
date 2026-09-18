from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

CARS_PATH = (
    BASE_DIR
    / "datasets"
    / "cars_dataset.csv"
)

SENATRAN_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "senatran"
    / "senatran_uf_features_2026-07.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "cars_dataset_enriched.csv"
)


STATE_MAP = {
    "ba": "BAHIA",
    "mg": "MINAS GERAIS",
    "pe": "PERNAMBUCO",
    "pr": "PARANA",
    "rj": "RIO DE JANEIRO",
    "rs": "RIO GRANDE DO SUL",
    "sp": "SAO PAULO",
}


SENATRAN_FEATURES = [
    "log_total_fleet",
    "car_share",
    "moto_share",
    "heavy_share",
    "implement_share",
]


def load_data():
    u = pd.read_csv(CARS_PATH)
    v = pd.read_csv(SENATRAN_PATH)

    return u, v


def build_enriched_dataset(u, v):
    u = u.copy()
    v = v.copy()

    u["senatran_state"] = u["state"].map(STATE_MAP)

    if u["senatran_state"].isnull().any():
        raise ValueError(
            "Existem estados no cars_dataset sem mapeamento SENATRAN."
        )

    v = v[
        ["state"] + SENATRAN_FEATURES
    ].copy()

    v = v.rename(
        columns={
            "state": "senatran_state",
            "log_total_fleet": "senatran_log_total_fleet",
            "car_share": "senatran_car_share",
            "moto_share": "senatran_moto_share",
            "heavy_share": "senatran_heavy_share",
            "implement_share": "senatran_implement_share",
        }
    )

    w = u.merge(
        v,
        on="senatran_state",
        how="left",
        validate="many_to_one",
    )

    return w


def validate_dataset(u):
    print("\n=== VALIDAÇÃO DATASET ENRIQUECIDO ===")

    print(f"Linhas: {len(u):,}")
    print(f"Colunas: {len(u.columns)}")

    print("\nNulos nas features SENATRAN:")

    print(
        u[
            [
                "senatran_log_total_fleet",
                "senatran_car_share",
                "senatran_moto_share",
                "senatran_heavy_share",
                "senatran_implement_share",
            ]
        ]
        .isnull()
        .sum()
        .to_string()
    )

    print("\nDistribuição por estado:")

    print(
        u[
            [
                "state",
                "senatran_state",
            ]
        ]
        .drop_duplicates()
        .sort_values("state")
        .to_string(index=False)
    )

    print("\nFeatures SENATRAN:")

    print(
        u[
            [
                "senatran_log_total_fleet",
                "senatran_car_share",
                "senatran_moto_share",
                "senatran_heavy_share",
                "senatran_implement_share",
            ]
        ]
        .describe()
        .to_string()
    )


def save_data(u):
    u.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"\nArquivo gerado: {OUTPUT_PATH}"
    )


def main():
    print("Carregando datasets...")

    u, v = load_data()

    print(
        f"Cars dataset: {len(u):,} registros"
    )

    print(
        f"SENATRAN: {len(v):,} registros"
    )

    w = build_enriched_dataset(u, v)

    validate_dataset(w)

    save_data(w)


if __name__ == "__main__":
    main()
