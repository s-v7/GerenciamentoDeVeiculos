from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "senatran"
    / "senatran_tipo_especie_eixos_2026-07.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "senatran"
    / "senatran_classificado_2026-07.csv"
)


VEHICLE_CLASS_MAP = {
    # Automóveis / veículos leves
    "AUTOMOVEL": "CARRO",
    "CAMINHONETE": "CARRO",
    "CAMIONETA": "CARRO",
    "UTILITARIO": "CARRO",

    # Motocicletas e similares
    "MOTOCICLETA": "MOTO",
    "MOTONETA": "MOTO",
    "CICLOMOTOR": "MOTO",
    "TRICICLO": "MOTO",
    "SIDE-CAR": "MOTO",
    "QUADRICICLO": "MOTO",

    # Veículos pesados
    "CAMINHAO": "PESADO",
    "CAMINHAO TRATOR": "PESADO",
    "ONIBUS": "PESADO",
    "MICROONIBUS": "PESADO",
    "MOTOR-CASA": "PESADO",
    "CHASSI/PLATAFORMA": "PESADO",
    "TRATOR DE RODAS": "PESADO",
    "TRATOR MISTO": "PESADO",
    "TRATOR DE ESTEIRAS": "PESADO",

    # Implementos rodoviários
    "REBOQUE": "IMPLEMENTO",
    "SEMI-REBOQUE": "IMPLEMENTO",

    # Outros veículos
    "BICICLETA": "OUTRO",
    "CHARRETE": "OUTRO",
    "CARRO DE MAO": "OUTRO",
    "BONDE": "OUTRO",
    "CARROCA": "OUTRO",

    # Dados sem classificação oficial suficiente
    "Sem Informação": "NAO_CLASSIFICADO",
    "Não Identificado": "NAO_CLASSIFICADO",
    "Não se Aplica": "NAO_CLASSIFICADO",
}


def load_data():
    return pd.read_csv(INPUT_PATH)


def classify_vehicle_type(u):
    u["vehicle_class"] = (
        u["vehicle_type"]
        .map(VEHICLE_CLASS_MAP)
        .fillna("NAO_CLASSIFICADO")
    )

    return u


def print_classification_distribution(u):
    print("\n=== DISTRIBUIÇÃO POR CLASSE ===\n")

    x = (
        u.groupby("vehicle_class")["vehicle_count"]
        .sum()
        .sort_values(ascending=False)
    )

    print(x)

    print("\n=== DISTRIBUIÇÃO POR TIPO ORIGINAL ===\n")

    x = (
        u.groupby(
            ["vehicle_class", "vehicle_type"]
        )["vehicle_count"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(x)


def print_unmapped_types(u):
    x = u.loc[
        ~u["vehicle_type"].isin(VEHICLE_CLASS_MAP.keys()),
        "vehicle_type",
    ].value_counts()

    print("\n=== TIPOS NÃO MAPEADOS ===\n")

    if x.empty:
        print("Nenhum tipo não mapeado.")
    else:
        print(x)


def save_data(u):
    u.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"\nArquivo classificado: {OUTPUT_PATH}"
    )


def main():
    print("Carregando dados SENATRAN...")

    u = load_data()

    print(
        f"Registros carregados: {len(u):,}"
    )

    u = classify_vehicle_type(u)

    print_classification_distribution(u)

    print_unmapped_types(u)

    save_data(u)


if __name__ == "__main__":
    main()
