from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = Path(__file__).resolve().parent.parent.parent

BASELINE_PATH = (
    BASE_DIR
    / "ai"
    / "datasets"
    / "cars_dataset.csv"
)

ENRICHED_PATH = (
    BASE_DIR
    / "ai"
    / "data"
    / "processed"
    / "cars_dataset_enriched.csv"
)


TARGET = "price"

BASE_FEATURES = [
    "make",
    "year",
    "engine_cc",
    "mileage_km",
    "doors",
    "fuel_type",
    "transmission",
    "body_type",
    "state",
]

SENATRAN_FEATURES = [
    "senatran_log_total_fleet",
    "senatran_car_share",
    "senatran_moto_share",
    "senatran_heavy_share",
    "senatran_implement_share",
]

NUMERICAL_FEATURES = [
    "year",
    "engine_cc",
    "mileage_km",
    "doors",
    "vehicle_age",
    "km_per_year",
]

CATEGORICAL_FEATURES = [
    "make",
    "fuel_type",
    "transmission",
    "body_type",
    "state",
]


def load_data():
    u = pd.read_csv(BASELINE_PATH)
    v = pd.read_csv(ENRICHED_PATH)

    return u, v


def split_data(u, features):
    w = u[features].copy()
    y = u[TARGET].copy()

    x_train, x_test, y_train, y_test = train_test_split(
        w,
        y,
        test_size=0.20,
        random_state=42,
    )

    return x_train, x_test, y_train, y_test


def prepare_features(u):
    u = u.copy()

    u["vehicle_age"] = 2025 - u["year"]

    u["km_per_year"] = (
        u["mileage_km"]
        / u["vehicle_age"].clip(lower=1)
    )

    return u


def build_preprocessor(numerical_features):
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
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )


def train_and_evaluate(x_train, x_test, y_train, y_test, features):
    u = prepare_features(x_train)
    v = prepare_features(x_test)

    numerical_features = (
        NUMERICAL_FEATURES
        + [
            feature
            for feature in SENATRAN_FEATURES
            if feature in features
        ]
    )

    preprocessor = build_preprocessor(
        numerical_features
    )

    x_train_transformed = preprocessor.fit_transform(u)
    x_test_transformed = preprocessor.transform(v)

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        x_train_transformed,
        y_train,
    )

    y_pred = model.predict(
        x_test_transformed
    )

    mae = mean_absolute_error(
        y_test,
        y_pred,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            y_pred,
        )
    )

    r2 = r2_score(
        y_test,
        y_pred,
    )

    return {
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "feature_count": x_train_transformed.shape[1],
    }


def print_results(name, results):
    print(f"\n=== {name} ===")

    print(
        f"MAE:  R$ {results['mae']:,.2f}"
    )

    print(
        f"RMSE: R$ {results['rmse']:,.2f}"
    )

    print(
        f"R²:   {results['r2']:.6f}"
    )

    print(
        f"Features transformadas: "
        f"{results['feature_count']}"
    )


def main():
    print("Carregando datasets...")

    u, v = load_data()

    print(
        f"Baseline: {len(u):,} registros"
    )

    print(
        f"Enriched: {len(v):,} registros"
    )

    print("\nPreparando divisões...")

    x_train_base, x_test_base, y_train_base, y_test_base = (
        split_data(
            u,
            BASE_FEATURES,
        )
    )

    x_train_enriched, x_test_enriched, y_train_enriched, y_test_enriched = (
        split_data(
            v,
            BASE_FEATURES + SENATRAN_FEATURES,
        )
    )

    print(
        f"Train: {len(x_train_base):,}"
    )

    print(
        f"Test:  {len(x_test_base):,}"
    )

    print("\nTreinando Baseline...")

    baseline = train_and_evaluate(
        x_train_base,
        x_test_base,
        y_train_base,
        y_test_base,
        BASE_FEATURES,
    )

    print("\nTreinando Baseline + SENATRAN...")

    enriched = train_and_evaluate(
        x_train_enriched,
        x_test_enriched,
        y_train_enriched,
        y_test_enriched,
        BASE_FEATURES + SENATRAN_FEATURES,
    )

    print_results(
        "BASELINE",
        baseline,
    )

    print_results(
        "BASELINE + SENATRAN",
        enriched,
    )

    print("\n=== DIFERENÇA ===")

    mae_delta = enriched["mae"] - baseline["mae"]
    rmse_delta = enriched["rmse"] - baseline["rmse"]
    r2_delta = enriched["r2"] - baseline["r2"]

    print(
        f"Δ MAE:  R$ {mae_delta:,.2f}"
    )

    print(
        f"Δ RMSE: R$ {rmse_delta:,.2f}"
    )

    print(
        f"Δ R²:   {r2_delta:+.6f}"
    )


if __name__ == "__main__":
    main()
