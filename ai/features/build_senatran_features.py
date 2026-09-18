from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "processed" / "senatran" / "senatran_uf_2026-07.csv"

OUTPUT_PATH = (
    BASE_DIR / "data" / "processed" / "senatran" / "senatran_uf_features_2026-07.csv"
)


def load_data():
    return pd.read_csv(INPUT_PATH)


def build_features(u):
    v = u.copy()

    w = v["total_fleet"]

    v["car_share"] = v["CARRO"] / w
    v["moto_share"] = v["MOTO"] / w
    v["heavy_share"] = v["PESADO"] / w
    v["implement_share"] = v["IMPLEMENTO"] / w
    v["unclassified_share"] = v["NAO_CLASSIFICADO"] / w
    v["other_share"] = v["OUTRO"] / w

    v["log_total_fleet"] = (1 + w).map(lambda x: __import__("math").log(x))

    return v


def validate_features(u):
    print("\n=== VALIDAÇÃO ===")

    print(f"Registros: {len(u):,}")

    print("\nNulos:")
    print(u.isnull().sum())

    print("\nShares:")
    print(
        u[
            [
                "car_share",
                "moto_share",
                "heavy_share",
                "implement_share",
                "unclassified_share",
                "other_share",
            ]
        ]
        .describe()
        .to_string()
    )

    x = u[
        [
            "car_share",
            "moto_share",
            "heavy_share",
            "implement_share",
            "unclassified_share",
            "other_share",
        ]
    ].sum(axis=1)

    print("\n=== SOMA DAS PARTICIPAÇÕES ===")
    print(x.describe().to_string())

    w = u[
        [
            "car_share",
            "moto_share",
            "heavy_share",
            "implement_share",
        ]
    ].sum(axis=1)

    print("\n=== COBERTURA DAS 4 CLASSES PRINCIPAIS ===")
    print(w.describe().to_string())

    if not ((x - 1).abs() < 1e-9).all():
        raise ValueError("As participações não somam aproximadamente 1.")

    print("Shares validados.")


def save_data(u):
    u.to_csv(OUTPUT_PATH, index=False)
    print(f"\nArquivo gerado: {OUTPUT_PATH}")


def main():
    print("Carregando SENATRAN por UF...")

    u = load_data()

    print(f"Registros: {len(u):,}")

    v = build_features(u)

    validate_features(v)

    print("\n=== FEATURES SENATRAN ===")
    print(
        v[
            [
                "state",
                "total_fleet",
                "car_share",
                "moto_share",
                "heavy_share",
                "implement_share",
                "log_total_fleet",
            ]
        ].to_string(index=False)
    )

    save_data(v)


if __name__ == "__main__":
    main()
