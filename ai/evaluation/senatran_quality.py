from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "ai" / "data" / "processed" / "senatran"


BRAND_MODEL_FILE = PROCESSED_DIR / "senatran_2026-07.csv"

TYPE_FILE = PROCESSED_DIR / "senatran_tipo_especie_eixos_2026-07.csv"


def load_data():
    u = pd.read_csv(
        BRAND_MODEL_FILE,
        usecols=[
            "state",
            "municipality",
            "make",
            "model",
            "manufacture_year",
            "vehicle_count",
        ],
    )

    v = pd.read_csv(
        TYPE_FILE,
        usecols=[
            "state",
            "municipality",
            "vehicle_type",
            "vehicle_species",
            "axles",
            "vehicle_count",
        ],
    )

    return u, v


def print_totals(u, v):
    print("\n=== TOTAIS ===\n")

    u_total = u["vehicle_count"].sum()
    v_total = v["vehicle_count"].sum()

    print(f"Marca/Modelo/Ano : {u_total:,}")

    print(f"Tipo/Espécie     : {v_total:,}")

    print(f"Diferença         : {v_total - u_total:,}")


def print_missing_state(u, v):
    print("\n=== SEM INFORMAÇÃO — UF ===\n")

    u_missing = u.loc[
        u["state"] == "Sem Informação",
        "vehicle_count",
    ].sum()

    v_missing = v.loc[
        v["state"] == "Sem Informação",
        "vehicle_count",
    ].sum()

    print(f"Marca/Modelo/Ano : {u_missing:,}")

    print(f"Tipo/Espécie     : {v_missing:,}")


def compare_by_state(u, v):
    print("\n=== COMPARAÇÃO POR UF ===\n")

    u_state = u.groupby("state")["vehicle_count"].sum().rename("brand_model_total")

    v_state = v.groupby("state")["vehicle_count"].sum().rename("type_total")

    x = pd.concat(
        [
            v_state,
            u_state,
        ],
        axis=1,
    ).fillna(0)

    x = x.loc[
        ~x.index.get_level_values("state").isin(
            [
                "Sem Informação",
                "Não se Aplica",
                "Não Identificado",
            ]
        )
    ]

    x["difference"] = x["type_total"] - x["brand_model_total"]

    x["difference_pct"] = x["difference"] / x["type_total"] * 100

    print(
        x.sort_values(
            "difference",
            ascending=False,
        ).to_string()
    )

    return x


def compare_by_municipality(u, v):
    print("\n=== COMPARAÇÃO POR MUNICÍPIO ===\n")

    u_municipality = (
        u.groupby(["state", "municipality"])["vehicle_count"]
        .sum()
        .rename("brand_model_total")
    )

    v_municipality = (
        v.groupby(["state", "municipality"])["vehicle_count"].sum().rename("type_total")
    )

    x = pd.concat(
        [
            v_municipality,
            u_municipality,
        ],
        axis=1,
    ).fillna(0)

    x = x.loc[
        ~x.index.get_level_values("state").isin(
            [
                "Sem Informação",
                "Não se Aplica",
                "Não Identificado",
            ]
        )
    ]

    x["difference"] = x["type_total"] - x["brand_model_total"]

    x["difference_pct"] = x["difference"] / x["type_total"] * 100

    x = x.replace(
        [float("inf"), -float("inf")],
        0,
    )

    print(
        "Municípios:",
        len(x),
    )

    print(
        "Diferença máxima (%):",
        round(
            x["difference_pct"].max(),
            4,
        ),
    )

    print(
        "Diferença média (%):",
        round(
            x["difference_pct"].mean(),
            4,
        ),
    )

    print(
        "Diferença mediana (%):",
        round(
            x["difference_pct"].median(),
            4,
        ),
    )

    print(
        "Municípios com diferença negativa:",
        int((x["difference"] < 0).sum()),
    )

    print(
        "Municípios > 5%:",
        int((x["difference_pct"] > 5).sum()),
    )

    print("\nTop diferenças:\n")

    print(
        x.sort_values(
            "difference_pct",
            ascending=False,
        )
        .head(20)
        .to_string()
    )

    return x


def print_duplicates(u, v):
    print("\n=== DUPLICIDADES ===\n")

    u_duplicates = u.duplicated(
        subset=[
            "state",
            "municipality",
            "make",
            "model",
            "manufacture_year",
        ]
    ).sum()

    v_duplicates = v.duplicated(
        subset=[
            "state",
            "municipality",
            "vehicle_type",
            "vehicle_species",
            "axles",
        ]
    ).sum()

    print(
        "Marca/Modelo/Ano:",
        int(u_duplicates),
    )

    print(
        "Tipo/Espécie/Eixos:",
        int(v_duplicates),
    )


def print_type_distribution(v):
    print("\n=== DISTRIBUIÇÃO POR TIPO ===\n")

    x = v.groupby("vehicle_type")["vehicle_count"].sum().sort_values(ascending=False)

    print(x.to_string())


def print_species_distribution(v):
    print("\n=== DISTRIBUIÇÃO POR ESPÉCIE ===\n")

    x = v.groupby("vehicle_species")["vehicle_count"].sum().sort_values(ascending=False)

    print(x.to_string())


def print_year_distribution(u):
    print("\n=== ANO DE FABRICAÇÃO ===\n")

    x = u.groupby("manufacture_year")["vehicle_count"].sum().sort_index()

    print(f"1900-1929: {x.loc[1900:1929].sum():,}")

    print(f"2030+: {x[x.index > 2026].sum():,}")

    print(f"2026: {x.get(2026, 0):,}")


def main():
    print("SENATRAN — AUDITORIA DE QUALIDADE")

    print(f"\nDataset 1: {BRAND_MODEL_FILE}")

    print(f"Dataset 2: {TYPE_FILE}")

    if not BRAND_MODEL_FILE.exists():
        raise SystemExit(f"Arquivo não encontrado:\n{BRAND_MODEL_FILE}")

    if not TYPE_FILE.exists():
        raise SystemExit(f"Arquivo não encontrado:\n{TYPE_FILE}")

    u, v = load_data()

    print_totals(u, v)

    print_missing_state(u, v)

    compare_by_state(u, v)

    compare_by_municipality(u, v)

    print_duplicates(u, v)

    print_type_distribution(v)

    print_species_distribution(v)

    print_year_distribution(u)

    print("\n=== AUDITORIA CONCLUÍDA ===\n")


if __name__ == "__main__":
    main()
