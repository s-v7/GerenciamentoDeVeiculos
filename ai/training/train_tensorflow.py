import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ai.features.build_features import CarFeaturePipeline


def train_tensorflow_model():
    processed_dir = BASE_DIR / "ai" / "datasets" / "processed"

    train_path = processed_dir / "train.csv"
    test_path = processed_dir / "test.csv"

    models_dir = BASE_DIR / "ai" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    if not train_path.exists() or not test_path.exists():
        raise FileNotFoundError(
            f"Dataset processado não encontrado em {processed_dir}. "
            "Execute: python3 ai/data/prepare_dataset.py"
        )

    print("Carregando dataset processado...")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    X_train_raw = train_df.drop(columns=["price"])
    y_train = train_df["price"].values

    X_test_raw = test_df.drop(columns=["price"])
    y_test = test_df["price"].values

    print(f"TRAIN: {len(X_train_raw)}")
    print(f"TEST : {len(X_test_raw)}")

    print("Processando features...")

    pipeline = CarFeaturePipeline()

    X_train, feature_names = pipeline.fit_transform(
        pd.concat(
            [
                X_train_raw,
                train_df[["price"]],
            ],
            axis=1,
        )
    )

    X_test = pipeline.transform(X_test_raw)

    print(f"Features de entrada: {X_train.shape[1]}")

    print("Construindo rede neural...")

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(X_train.shape[1],)),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1),
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="mse",
        metrics=["mae"],
    )

    model.summary()

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=15,
        restore_best_weights=True,
    )

    print("\nTreinando TensorFlow...")

    history = model.fit(
        X_train,
        y_train,
        validation_split=0.2,
        epochs=400,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=1,
    )

    print("\nRealizando previsões...")

    y_pred = model.predict(X_test, verbose=0).flatten()

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("\n================= Métricas TensorFlow =================")
    print(f"MAE  : R$ {mae:,.2f}")
    print(f"RMSE : R$ {rmse:,.2f}")
    print(f"R²   : {r2:.4f}")

    model_path = models_dir / "car_price_tensorflow.keras"

    model.save(model_path)

    print(f"\nModelo salvo em: {model_path}")
    print(f"Épocas executadas: {len(history.history['loss'])}")

    return model, pipeline


if __name__ == "__main__":
    train_tensorflow_model()
