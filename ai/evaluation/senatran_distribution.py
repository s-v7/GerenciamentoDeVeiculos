from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "senatran"
    / "senatran_municipio_2026-07.csv"
)


def load_data():
    return pd.read_csv(INPUT_PATH)


def add_shares(u):
    x = u.copy()

    x["car_share"] = x["CARRO"] / x["total_fleet"]
    x["moto_share"] = x["MOTO"] / x["total_fleet"]
    x["heavy_share"] = x["PESADO"] / x["total_fleet"]
    x["implement_share"] = x["IMPLEMENTO"] / x["total_fleet"]

    return x


def print_distribution(u):
    print("\n=== ESTATÍSTICAS DA FROTA MUNICIPAL ===")
    print(
        u[
            [
                "total_fleet",
                "CARRO",
                "MOTO",
                "PESADO",
                "IMPLEMENTO",
            ]
        ].describe().to_string()
    )


def print_top_fleet(u):
    print("\n=== TOP 20 - FROTA TOTAL ===")

    x = u.nlargest(20, "total_fleet")

    print(
        x[
            [
                "state",
                "municipality",
                "total_fleet",
                "CARRO",
                "MOTO",
                "PESADO",
                "IMPLEMENTO",
            ]
        ].to_string(index=False)
    )


def print_top_cars(u):
    print("\n=== TOP 20 - CARROS ===")

    x = u.nlargest(20, "CARRO")

    print(
        x[
            [
                "state",
                "municipality",
                "CARRO",
                "total_fleet",
                "car_share",
            ]
        ].to_string(index=False)
    )


def print_top_motos(u):
    print("\n=== TOP 20 - MOTOS ===")

    x = u.nlargest(20, "MOTO")

    print(
        x[
            [
                "state",
                "municipality",
                "MOTO",
                "total_fleet",
                "moto_share",
            ]
        ].to_string(index=False)
    )


def print_top_heavy(u):
    print("\n=== TOP 20 - PESADOS ===")

    x = u.nlargest(20, "PESADO")

    print(
        x[
            [
                "state",
                "municipality",
                "PESADO",
                "total_fleet",
                "heavy_share",
            ]
        ].to_string(index=False)
    )


def print_top_implement(u):
    print("\n=== TOP 20 - IMPLEMENTOS ===")

    x = u.nlargest(20, "IMPLEMENTO")

    print(
        x[
            [
                "state",
                "municipality",
                "IMPLEMENTO",
                "total_fleet",
                "implement_share",
            ]
        ].to_string(index=False)
    )


def print_high_moto_share(u):
    print("\n=== MAIOR CONCENTRAÇÃO DE MOTOS ===")

    # Evita municípios muito pequenos dominarem a análise.
    x = u.loc[u["total_fleet"] >= 1000].nlargest(
        20,
        "moto_share",
    )

    print(
        x[
            [
                "state",
                "municipality",
                "total_fleet",
                "MOTO",
                "moto_share",
            ]
        ].to_string(index=False)
    )


def print_high_car_share(u):
    print("\n=== MAIOR CONCENTRAÇÃO DE CARROS ===")

    x = u.loc[u["total_fleet"] >= 1000].nlargest(
        20,
        "car_share",
    )

    print(
        x[
            [
                "state",
                "municipality",
                "total_fleet",
                "CARRO",
                "car_share",
            ]
        ].to_string(index=False)
    )


def print_smallest_municipalities(u):
    print("\n=== 20 MENORES FROTAS ===")

    x = u.nsmallest(20, "total_fleet")

    print(
        x[
            [
                "state",
                "municipality",
                "total_fleet",
                "CARRO",
                "MOTO",
            ]
        ].to_string(index=False)
    )


def main():
    print("Carregando SENATRAN municipal...")

    u = load_data()

    print(f"Registros: {len(u):,}")

    u = add_shares(u)

    print_distribution(u)
    print_top_fleet(u)
    print_top_cars(u)
    print_top_motos(u)
    print_top_heavy(u)
    print_top_implement(u)
    print_high_moto_share(u)
    print_high_car_share(u)
    print_smallest_municipalities(u)


if __name__ == "__main__":
    main()
