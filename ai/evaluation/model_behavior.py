import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
import tensorflow as tf

from ai.features.build_features import CarFeaturePipeline


def predict_price(model, pipeline, sample_data):
    u = pd.DataFrame([sample_data])
    v = pipeline.transform(u)
    w = model.predict(v, verbose=0).flatten()[0]
    return float(w)


def compare_scenarios(title, scenarios, model, pipeline):
    print(f"\n=== {title} ===")

    u_base = scenarios[0][1]
    v_base_price = predict_price(model, pipeline, u_base)

    print(f"Base: R$ {v_base_price:,.2f}\n")

    for name, car in scenarios:
        w_price = predict_price(model, pipeline, car)
        x_difference = w_price - v_base_price

        print(
            f"{name:<35} "
            f"R$ {w_price:>12,.2f} "
            f"({x_difference:+,.2f})"
        )


def main():
    models_dir = BASE_DIR / "ai" / "models"
    data_dir = BASE_DIR / "ai" / "datasets" / "processed"

    model_path = models_dir / "car_price_tensorflow.keras"
    train_path = data_dir / "train.csv"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Modelo TensorFlow não encontrado: {model_path}"
        )

    if not train_path.exists():
        raise FileNotFoundError(
            f"Dataset de treino não encontrado: {train_path}"
        )

    train = pd.read_csv(train_path)

    model = tf.keras.models.load_model(model_path)

    pipeline = CarFeaturePipeline()
    pipeline.fit_transform(train)

    base_car = {
        "make": "Toyota",
        "year": 2020,
        "engine_cc": 2000,
        "mileage_km": 50000,
        "doors": 4,
        "fuel_type": "flex",
        "transmission": "automatico",
        "body_type": "sedan",
        "state": "SP",
    }

    compare_scenarios(
        "IMPACTO DO ANO",
        [
            ("2020", {**base_car, "year": 2020}),
            ("2023", {**base_car, "year": 2023}),
            ("2025", {**base_car, "year": 2025}),
            ("2015", {**base_car, "year": 2015}),
        ],
        model,
        pipeline,
    )

    compare_scenarios(
        "IMPACTO DA QUILOMETRAGEM",
        [
            ("50.000 km", {**base_car, "mileage_km": 50000}),
            ("100.000 km", {**base_car, "mileage_km": 100000}),
            ("150.000 km", {**base_car, "mileage_km": 150000}),
            ("200.000 km", {**base_car, "mileage_km": 200000}),
        ],
        model,
        pipeline,
    )

    compare_scenarios(
        "IMPACTO DA MARCA",
        [
            ("Toyota", {**base_car, "make": "Toyota"}),
            ("Honda", {**base_car, "make": "Honda"}),
            ("Volkswagen", {**base_car, "make": "Volkswagen"}),
            ("Chevrolet", {**base_car, "make": "Chevrolet"}),
            ("Ford", {**base_car, "make": "Ford"}),
            ("Hyundai", {**base_car, "make": "Hyundai"}),
            ("BMW", {**base_car, "make": "BMW"}),
        ],
        model,
        pipeline,
    )

    compare_scenarios(
        "IMPACTO DO CÂMBIO",
        [
            ("Automático", {**base_car, "transmission": "automatico"}),
            ("Manual", {**base_car, "transmission": "manual"}),
        ],
        model,
        pipeline,
    )

    compare_scenarios(
        "IMPACTO DO MOTOR",
        [
            ("2.0L", {**base_car, "engine_cc": 2000}),
            ("1.0L", {**base_car, "engine_cc": 1000}),
            ("1.6L", {**base_car, "engine_cc": 1600}),
            ("3.0L", {**base_car, "engine_cc": 3000}),
        ],
        model,
        pipeline,
    )


if __name__ == "__main__":
    main()
