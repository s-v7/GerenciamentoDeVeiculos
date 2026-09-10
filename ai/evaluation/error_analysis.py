import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


import joblib
import numpy as np
import pandas as pd

#from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from ai.features.build_features import CarFeaturePipeline

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "ai" / "datasets" / "processed"
MODEL_DIR = BASE_DIR / "ai" / "models"

def analyze():
    train = pd.read_csv(DATA_DIR / "train.csv")
    test = pd.read_csv(DATA_DIR / "test.csv")

    u_train = train.drop(columns=["price"])
    v_train = train["price"]

    u_test = test.drop(columns=["price"])
    v_test = test["price"]

    pipeline = joblib.load(MODEL_DIR / "feature_pipeline.pkl")
    model = joblib.load(MODEL_DIR / "car_price_model.pkl")

    u_train_transformed, _ = pipeline.fit_transform(
        pd.concat([u_train, v_train], axis=1)
    )

    u_test_transformed = pipeline.transform(u_test)
    model.fit(u_train_transformed, v_train)

    predictions = model.predict(u_test_transformed)

    result = test.copy()
    result["predicted_price"] = predictions
    result["absolute_error"] = np.abs(
        result["price"] - result["predicted_price"]
    )
    result["error_pct"] = (
        result["absolute_error"] / result["price"]
    ) * 100

    print("\n======= MÉTRICAS ========")
    print(f"[MAE] : R$ {mean_absolute_error(v_test, predictions):,.2f}")
    print(f"[RMSE] : R$ {np.sqrt(mean_squared_error(v_test, predictions)):,.2f}")
    print(f"R² : {r2_score(v_test, predictions):,.4f}")

    print("\n=== ERROR MÉDIO POR FAIXA DE PREÇO ===")
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
            mae=("absolute_error", "mean"),
            mean_error_pct=("error_pct", "mean"),
        )
        .round(2)
    )

    print(summary.to_string())
    print("\n=== 10 MAIORES ERROS ===")
    columns = [
        "year",
        "engine_cc",
        "mileage_km",
        "fuel_type",
        "transmission",
        "body_type",
        "state",
        "price",
        "predicted_price",
        "absolute_error",
        "error_pct",
    ]

    print(
        result.nlargest(10, "absolute_error")[columns]
        .round(2)
        .to_string(index=False)
    )
if __name__ == "__main__":
    analyze()
