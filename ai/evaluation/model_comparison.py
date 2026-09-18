import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from ai.features.build_features import CarFeaturePipeline


TARGET = "price"


def evaluate_model(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    return mae, rmse, r2


def main():
    print("Carregando dataset...")

    dataset_path = BASE_DIR / "ai" / "datasets" / "cars_dataset.csv"

    u = pd.read_csv(dataset_path)

    print(f"Registros: {len(u):,}")

    x = u.drop(columns=[TARGET])
    y = u[TARGET]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        random_state=42,
    )

    print("\n=== SPLIT ===")
    print(f"TRAIN: {len(x_train):,}")
    print(f"TEST : {len(x_test):,}")

    # ==========================================================
    # FEATURE ENGINEERING
    # ==========================================================

    print("\nProcessando features...")

    v = CarFeaturePipeline()

    w_train, feature_names = v.fit_transform(
        pd.concat(
            [
                x_train,
                y_train,
            ],
            axis=1,
        )
    )

    w_test = v.transform(x_test)

    print(f"Features transformadas: {w_train.shape[1]}")

    # ==========================================================
    # RANDOM FOREST
    # ==========================================================

    print("\n=== RANDOM FOREST ===")

    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    rf.fit(w_train, y_train)

    y_pred_rf = rf.predict(w_test)

    mae_rf, rmse_rf, r2_rf = evaluate_model(
        y_test,
        y_pred_rf,
    )

    print(f"MAE :  R$ {mae_rf:,.2f}")
    print(f"RMSE:  R$ {rmse_rf:,.2f}")
    print(f"R²  :  {r2_rf:.6f}")

    # ==========================================================
    # TENSORFLOW
    # ==========================================================

    print("\n=== TENSORFLOW ===")

    tf.keras.utils.set_random_seed(42)

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(w_train.shape[1],)),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1),
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="mse",
        metrics=["mae"],
    )

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=15,
        restore_best_weights=True,
    )

    model.fit(
        w_train,
        y_train.values,
        validation_split=0.2,
        epochs=400,
        batch_size=32,
        callbacks=[early_stopping],
        verbose=0,
    )

    y_pred_tf = model.predict(
        w_test,
        verbose=0,
    ).flatten()

    mae_tf, rmse_tf, r2_tf = evaluate_model(
        y_test,
        y_pred_tf,
    )

    print(f"MAE :  R$ {mae_tf:,.2f}")
    print(f"RMSE:  R$ {rmse_tf:,.2f}")
    print(f"R²  :  {r2_tf:.6f}")

    # ==========================================================
    # COMPARAÇÃO
    # ==========================================================

    print("\n=== COMPARAÇÃO ===")

    u_result = pd.DataFrame(
        [
            {
                "model": "Random Forest",
                "mae": mae_rf,
                "rmse": rmse_rf,
                "r2": r2_rf,
            },
            {
                "model": "TensorFlow",
                "mae": mae_tf,
                "rmse": rmse_tf,
                "r2": r2_tf,
            },
        ]
    )

    print(u_result.to_string(index=False))

    print("\n=== DIFERENÇA TF - RF ===")

    print(f"Δ MAE :  R$ {mae_tf - mae_rf:,.2f}")
    print(f"Δ RMSE:  R$ {rmse_tf - rmse_rf:,.2f}")
    print(f"Δ R²  :  {r2_tf - r2_rf:+.6f}")


if __name__ == "__main__":
    main()
