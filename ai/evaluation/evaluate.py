import sys
from pathlib import Path

# Garantir imports do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
import pandas as pd

def predict_car_price(sample_data: dict) -> float:
    """Carrega os artefatos e estima o preco para um dicionario de atributos de veiculo."""
    models_dir = BASE_DIR / "ai" / "models"
    model_path = models_dir / "car_price_model.pkl"
    pipeline_path = models_dir / "feature_pipeline.pkl"
    
    if not model_path.exists() or not pipeline_path.exists():
        raise FileNotFoundError("Artefatos do modelo nao encontrados. Execute ai/training/train.py primeiro.")
        
    model = joblib.load(model_path)
    pipeline = joblib.load(pipeline_path)
    
    df_sample = pd.DataFrame([sample_data])
    X_trans = pipeline.transform(df_sample)
    pred_price = model.predict(X_trans)[0]
    
    return float(pred_price)

if __name__ == "__main__":
    test_cars = [
        {
            "make": "Toyota",
            "year": 2023,
            "engine_cc": 2000,
            "mileage_km": 25000,
            "doors": 4,
            "fuel_type": "flex",
            "transmission": "automatico",
            "body_type": "sedan",
            "state": "SP"
        },
        {
            "make": "Volkswagen",
            "year": 2012,
            "engine_cc": 1000,
            "mileage_km": 140000,
            "doors": 4,
            "fuel_type": "flex",
            "transmission": "manual",
            "body_type": "hatch",
            "state": "RJ"
        },
        {
            "make": "BMW",
            "year": 2022,
            "engine_cc": 3000,
            "mileage_km": 18000,
            "doors": 4,
            "fuel_type": "gasolina",
            "transmission": "automatico",
            "body_type": "suv",
            "state": "SP"
        }
    ]
    
    print(" Testando inferencias de precificacao com o modelo carregado...\n")
    for idx, car in enumerate(test_cars, 1):
        estimated_price = predict_car_price(car)
        print(f"--- Veiculo #{idx} ---")
        print(f"{car['year']} {car['make']} {car['engine_cc']/1000:.1f}L {car['body_type']} ({car['transmission']})")
        print(f"Estado: {car['state']} | KM: {car['mileage_km']:,}")
        print(f"Preco Estimado: R$ {estimated_price:,.2f}\n")
