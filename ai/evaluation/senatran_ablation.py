from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATASET_PATH = (
    BASE_DIR
    / "ai"
    / "data"
    / "processed"
    / "cars_dataset_enriched.csv"
)

TARGET = "price"

VEHICLE_FEATURES = [
    "make",
    "year",
    "engine_cc",
    "mileage_km",
    "doors",
    "fuel_type",
    "transmission",
    "body_type",
]

STATE_FEATURE = [
    "state",
]

SENATRAN_FEATURES = [
    "senatran_log_total_fleet",
    "senatran_car_share",
    "senatran_moto_share",
    "senatran_heavy_share",
    "senatran_implement_share",
]

NUMERICAL_BASE = [
    "year",
    "engine_cc",
    "mileage_km",
    "doors",
    "vehicle_age",
    "km_per_year",
]

CATEGORICAL_BASE = [
    "make",
    "fuel_type",
    "transmission",
    "body_type",
]


def load_data():
    return pd.read_csv(DATASET_PATH)


def prepare_features(u):
    u = u.copy()

    u["vehicle_age"] = 2025 - u["year"]

    u["km_per_year"] = (
        u["mileage_km"]
        / u["vehicle_age"].clip(lower=1)
    )

    return u


def build_preprocessor(numerical_features, categorical_features):
    return ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                numerical_features,
            ),
            (
                "cat",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
                categorical_features,
            ),
        ],
        remainder="drop",
    )


def train_and_evaluate(
    u_train,
    u_test,
    y_train,
    y_test,
    numerical_features,
    categorical_features,
):
    v = prepare_features(u_train)
    w = prepare_features(u_test)

    preprocessor = build_preprocessor(
        numerical_features,
        categorical_features,
    )

    v = preprocessor.fit_transform(v)
    w = preprocessor.transform(w)

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(v, y_train)

    x = model.predict(w)

    mae = mean_absolute_error(
        y_test,
        x,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            x,
        )
    )

    r2 = r2_score(
        y_test,
        x,
    )

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "features": v.shape[1],
    }


def run_experiment(
    name,
    u_train,
    u_test,
    y_train,
    y_test,
    features,
    numerical_features,
    categorical_features,
):
    v = u_train[features].copy()
    w = u_test[features].copy()

    result = train_and_evaluate(
        v,
        w,
        y_train,
        y_test,
        numerical_features,
        categorical_features,
    )

    result["name"] = name

    return result


def main():
    print("Carregando dataset enriquecido...")

    u = load_data()

    print(f"Registros: {len(u):,}")

    y = u[TARGET].copy()

    x = u.drop(
        columns=[TARGET]
    )

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        random_state=42,
    )

    print("\n=== SPLIT ===")
    print(f"TRAIN: {len(x_train):,}")
    print(f"TEST:  {len(x_test):,}")

    experiments = [
        {
            "name": "A — Veículo",
            "features": VEHICLE_FEATURES,
            "numerical": NUMERICAL_BASE,
            "categorical": CATEGORICAL_BASE,
        },
        {
            "name": "B — Veículo + Estado",
            "features": VEHICLE_FEATURES + STATE_FEATURE,
            "numerical": NUMERICAL_BASE,
            "categorical": CATEGORICAL_BASE + STATE_FEATURE,
        },
        {
            "name": "C — Veículo + SENATRAN",
            "features": VEHICLE_FEATURES + SENATRAN_FEATURES,
            "numerical": NUMERICAL_BASE + SENATRAN_FEATURES,
            "categorical": CATEGORICAL_BASE,
        },
        {
            "name": "D — Veículo + Estado + SENATRAN",
            "features": (
                VEHICLE_FEATURES
                + STATE_FEATURE
                + SENATRAN_FEATURES
            ),
            "numerical": NUMERICAL_BASE + SENATRAN_FEATURES,
            "categorical": CATEGORICAL_BASE + STATE_FEATURE,
        },
    ]

    results = []

    for experiment in experiments:
        print(
            f"\nExecutando {experiment['name']}..."
        )

        result = run_experiment(
            experiment["name"],
            x_train,
            x_test,
            y_train,
            y_test,
            experiment["features"],
            experiment["numerical"],
            experiment["categorical"],
        )

        results.append(result)

    v = pd.DataFrame(results)

    v = v[
        [
            "name",
            "mae",
            "rmse",
            "r2",
            "features",
        ]
    ]

    print("\n=== RESULTADOS ===")
    print(v.to_string(index=False))

    print("\n=== COMPARAÇÃO COM O CENÁRIO A ===")

    u = v.iloc[0]

    for _, w in v.iterrows():
        print(
            f"\n{w['name']}"
        )

        print(
            f"Δ MAE:  R$ {w['mae'] - u['mae']:,.2f}"
        )

        print(
            f"Δ RMSE: R$ {w['rmse'] - u['rmse']:,.2f}"
        )

        print(
            f"Δ R²:   {w['r2'] - u['r2']:+.6f}"
        )


if __name__ == "__main__":
    main()
