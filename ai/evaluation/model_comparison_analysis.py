import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from ai.features.build_features import CarFeaturePipeline

TARGET = "price"


def main():
    print("Carregando dataset...")

    dataset_path = BASE_DIR / "ai" / "datasets" / "cars_dataset.csv"

    u = pd.read_csv(dataset_path)

    x = u.drop(columns=[TARGET])
    y = u[TARGET]

    from sklearn.model_selection import train_test_split

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        random_state=42,
    )

    print(f"TRAIN: {len(x_train):,}")
    print(f"TEST : {len(x_test):,}")

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

    print("\nTreinando Random Forest...")

    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    rf.fit(w_train, y_train)

    y_pred_rf = rf.predict(w_test)

    print("Treinando TensorFlow...")

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

    z = x_test.copy()

    z["actual_price"] = y_test.values
    z["rf_prediction"] = y_pred_rf
    z["tf_prediction"] = y_pred_tf

    z["rf_error"] = (
        z["rf_prediction"] - z["actual_price"]
    )

    z["tf_error"] = (
        z["tf_prediction"] - z["actual_price"]
    )

    z["rf_abs_error"] = z["rf_error"].abs()
    z["tf_abs_error"] = z["tf_error"].abs()

    z["tf_better"] = (
        z["tf_abs_error"] < z["rf_abs_error"]
    )

    z["error_difference"] = (
        z["rf_abs_error"] - z["tf_abs_error"]
    )

    print("\n=== ERROR ANALYSIS ===")

    print(
        f"MAE RF: R$ "
        f"{mean_absolute_error(y_test, y_pred_rf):,.2f}"
    )

    print(
        f"MAE TF: R$ "
        f"{mean_absolute_error(y_test, y_pred_tf):,.2f}"
    )

    print(
        f"\nTensorFlow melhor em: "
        f"{z['tf_better'].sum()} / {len(z)} veículos"
    )

    print(
        f"Random Forest melhor em: "
        f"{(~z['tf_better']).sum()} / {len(z)} veículos"
    )

    print("\n=== TOP 10 ERROS RANDOM FOREST ===")

    cols = [
        "make",
        "year",
        "mileage_km",
        "state",
        "actual_price",
        "rf_prediction",
        "rf_abs_error",
        "tf_prediction",
        "tf_abs_error",
    ]

    print(
        z.nlargest(10, "rf_abs_error")[cols]
        .to_string(index=False)
    )

    print("\n=== TOP 10 ERROS TENSORFLOW ===")

    print(
        z.nlargest(10, "tf_abs_error")[cols]
        .to_string(index=False)
    )
    print("\n=== TOP 10 CASOS EM QUE TENSORFLOW GANHOU ===")

    print(
        z.nlargest(10, "error_difference")[cols]
        .to_string(index=False)
    )
    print("\n=== MAE POR MARCA ===")

    z["rf_abs_error"] = z["rf_abs_error"].astype(float)
    z["tf_abs_error"] = z["tf_abs_error"].astype(float)

    q = (
        z.groupby("make")
        .agg(
            rf_mae=("rf_abs_error", "mean"),
            tf_mae=("tf_abs_error", "mean"),
            samples=("make", "size"),
        )
        .sort_values("tf_mae")
    )

    print(q.to_string())
    output_path = (
        BASE_DIR
        / "ai"
        / "data"
        / "processed"
        / "model_comparison_analysis.csv"
    )

    z.to_csv(
        output_path,
        index=False,
    )

    print(
        f"\nArquivo gerado:\n{output_path}"
    )


if __name__ == "__main__":
    main()
