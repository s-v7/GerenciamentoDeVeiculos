from pathlib import Path

import json
import pandas as pd
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = BASE_DIR / "ai" / "datasets" / "cars_dataset.csv"
OUTPUT_DIR = BASE_DIR / "ai" / "datasets" / "processed"

FEATURES = [
    "year",
    "engine_cc",
    "mileage_km",
    "doors",
    "fuel_type",
    "transmission",
    "body_type",
    "state",
]

TARGET = "price"


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATASET_PATH)

    required = FEATURES + [TARGET]
    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(f"Colunas ausentes: {missing}")

    if df[required].isnull().any().any():
        raise ValueError("Dataset contém valores nulos")

    return df


def prepare_dataset():
    df = load_dataset()

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    train = X_train.copy()
    train[TARGET] = y_train

    test = X_test.copy()
    test[TARGET] = y_test

    train.to_csv(OUTPUT_DIR / "train.csv", index=False)
    test.to_csv(OUTPUT_DIR / "test.csv", index=False)

    metadata = {
        "dataset": DATASET_PATH.name,
        "total_rows": len(df),
        "train_rows": len(train),
        "test_rows": len(test),
        "features": FEATURES,
        "target": TARGET,
        "test_size": 0.20,
        "random_state": 42,
    }

    with open(OUTPUT_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = prepare_dataset()

    print("Dataset preparado.")
    print(f"TRAIN: {len(X_train)}")
    print(f"TEST:  {len(X_test)}")
    print(f"OUTPUT: {OUTPUT_DIR}")
