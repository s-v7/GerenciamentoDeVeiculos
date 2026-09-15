import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ai.features.build_features import CarFeaturePipeline

DATA_DIR = BASE_DIR / "ai" / "datasets" / "processed"
MODEL_DIR = BASE_DIR / "ai" / "models"


def calculate_metrics(y_true, predictions):
    return {
        "mae": mean_absolute_error(y_true, predictions),
        "rmse": np.sqrt(mean_squared_error(y_true, predictions)),
        "r2": r2_score(y_true, predictions),
    }


def print_metrics(name, metrics):
    print(f"\n=== {name} ===")
    print(f"MAE  : R$ {metrics['mae']:,.2f}")
    print(f"RMSE : R$ {metrics['rmse']:,.2f}")
    print(f"R²   : {metrics['r2']:.4f}")


def tensorflow_permutation_importance(
    model,
    u_test_transformed,
    v_test,
    feature_names,
    repetitions=50,
):
    baseline_predictions = model.predict(
        u_test_transformed,
        verbose=0,
    ).flatten()

    baseline_mae = mean_absolute_error(
        v_test,
        baseline_predictions,
    )

    results = []

    for feature_index, feature_name in enumerate(feature_names):
        scores = []

        for _ in range(repetitions):
            u_permuted = u_test_transformed.copy()

            np.random.shuffle(u_permuted[:, feature_index])

            predictions = model.predict(
                u_permuted,
                verbose=0,
            ).flatten()

            mae = mean_absolute_error(
                v_test,
                predictions,
            )

            scores.append(mae)

        importance = np.mean(scores) - baseline_mae

        importance_pct = (
            importance / baseline_mae
        ) * 100

        results.append(
            {
                "feature": feature_name,
                "importance": importance,
                "importance_pct": importance_pct,
            }
        )

    return pd.DataFrame(results).sort_values(
        "importance",
        ascending=False,
    )


def analyze():
    train = pd.read_csv(DATA_DIR / "train.csv")
    test = pd.read_csv(DATA_DIR / "test.csv")

    x_train = train.drop(columns=["price"])
    y_train = train["price"]

    x_test = test.drop(columns=["price"])
    y_test = test["price"]

    print("Processando features...")

    pipeline = CarFeaturePipeline()

    x_train_transformed, feature_names = pipeline.fit_transform(
        pd.concat([x_train, train[["price"]]], axis=1)
    )

    x_test_transformed = pipeline.transform(x_test)

    print(f"Features: {len(feature_names)}")

    rf_model = joblib.load(MODEL_DIR / "car_price_model.pkl")
    rf_model.fit(x_train_transformed, y_train)
    rf_predictions = rf_model.predict(x_test_transformed)
    rf_metrics = calculate_metrics(y_test, rf_predictions)
    tensorflow_model = tf.keras.models.load_model(
        MODEL_DIR / "car_price_tensorflow.keras"
    )

    tf_predictions = tensorflow_model.predict(
        x_test_transformed,
        verbose=0,
    ).flatten()

    tf_metrics = calculate_metrics(y_test, tf_predictions)
    print("\n=== TENSORFLOW — PERMUTATION IMPORTANCE ===")
    tf_importance = tensorflow_permutation_importance(
        tensorflow_model,
        x_test_transformed,
        y_test,
        feature_names,
    )
    print(tf_importance.round(4).to_string(index=False))
    print("\n==========================================")
    print("       COMPARAÇÃO DOS MODELOS")
    print("==========================================")

    print_metrics("Random Forest", rf_metrics)
    print_metrics("TensorFlow", tf_metrics)

    mae_improvement = (
        (rf_metrics["mae"] - tf_metrics["mae"])
        / rf_metrics["mae"]
    ) * 100

    rmse_improvement = (
        (rf_metrics["rmse"] - tf_metrics["rmse"])
        / rf_metrics["rmse"]
    ) * 100

    print("\n=== MELHORIA TensorFlow vs Random Forest ===")
    print(f"MAE  : {mae_improvement:.2f}%")
    print(f"RMSE : {rmse_improvement:.2f}%")
    print(f"R²   : {tf_metrics['r2'] - rf_metrics['r2']:+.4f}")

    result = test.copy()

    result["rf_predicted_price"] = rf_predictions
    result["tf_predicted_price"] = tf_predictions

    result["rf_absolute_error"] = np.abs(
        result["price"] - result["rf_predicted_price"]
    )

    result["tf_absolute_error"] = np.abs(
        result["price"] - result["tf_predicted_price"]
    )

    result["rf_error_pct"] = (
        result["rf_absolute_error"] / result["price"]
    ) * 100

    result["tf_error_pct"] = (
        result["tf_absolute_error"] / result["price"]
    ) * 100

    result["price_range"] = pd.cut(
        result["price"],
        bins=[0, 40000, 70000, 100000, 130000, float("inf")],
        labels=[
            "0-40k",
            "40-70k",
            "70-100k",
            "100-130k",
            "130k+",
        ],
    )

    summary = (
        result.groupby("price_range", observed=True)
        .agg(
            samples=("price", "size"),
            rf_mae=("rf_absolute_error", "mean"),
            tf_mae=("tf_absolute_error", "mean"),
            rf_error_pct=("rf_error_pct", "mean"),
            tf_error_pct=("tf_error_pct", "mean"),
        )
        .round(2)
    )

    print("\n=== ERROR MÉDIO POR FAIXA DE PREÇO ===")
    print(summary.to_string())

    print("\n=== 10 MAIORES ERROS — TENSORFLOW ===")

    columns = [
        "make",
        "year",
        "engine_cc",
        "mileage_km",
        "fuel_type",
        "transmission",
        "body_type",
        "state",
        "price",
        "tf_predicted_price",
        "tf_absolute_error",
        "tf_error_pct",
    ]

    print(
        result.nlargest(10, "tf_absolute_error")[columns]
        .round(2)
        .to_string(index=False)
    )

    result["winner"] = np.where(
        result["tf_absolute_error"] < result["rf_absolute_error"],
        "tensorflow",
        "random_forest",
    )

    winners = result["winner"].value_counts()

    print("\n=== VITÓRIA POR AMOSTRA ===")
    print(winners.to_string())


if __name__ == "__main__":
    analyze()

