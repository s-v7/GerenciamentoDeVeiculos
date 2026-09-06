from pathlib import Path
import json
import pandas as pd

from ai.data.prepare_dataset import prepare_dataset


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "ai" / "datasets" / "processed"


def test_dataset_split():
    X_train, X_test, y_train, y_test = prepare_dataset()

    assert len(X_train) == 1200
    assert len(X_test) == 300
    assert len(y_train) == 1200
    assert len(y_test) == 300


def test_processed_artifacts():
    train_path = PROCESSED_DIR / "train.csv"
    test_path = PROCESSED_DIR / "test.csv"
    metadata_path = PROCESSED_DIR / "metadata.json"

    assert train_path.exists()
    assert test_path.exists()
    assert metadata_path.exists()

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    assert len(train) == 1200
    assert len(test) == 300

    with open(metadata_path, encoding="utf-8") as f:
        metadata = json.load(f)

    assert metadata["total_rows"] == 1500
    assert metadata["train_rows"] == 1200
    assert metadata["test_rows"] == 300
    assert metadata["target"] == "price"
