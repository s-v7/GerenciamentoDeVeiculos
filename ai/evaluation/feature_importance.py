import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
import pandas as pd


DATA_DIR = BASE_DIR / "ai" / "datasets" / "processed"
MODEL_DIR = BASE_DIR / "ai" / "models"


train = pd.read_csv(DATA_DIR / "train.csv")

X = train.drop(columns=["price"])
y = train["price"]

pipeline = joblib.load(MODEL_DIR / "feature_pipeline.pkl")
model = joblib.load(MODEL_DIR / "car_price_model.pkl")

X_transformed, feature_names = pipeline.fit_transform(
    pd.concat([X, y], axis=1)
)

model.fit(X_transformed, y)

importance = pd.DataFrame({
    "feature": feature_names,
    "importance": model.feature_importances_,
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

print("\n=== FEATURE IMPORTANCE ===")
print(importance.to_string(index=False))
