import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ai.features.build_features import CarFeaturePipeline

def train_model():
    dataset_path = BASE_DIR / "ai" / "datasets" / "cars_dataset.csv"
    models_dir = BASE_DIR / "ai" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset não encontrado em {dataset_path}. Execute generate_synthetic_data.py.")

    print("Carregando dataset ...")
    df = pd.read_csv(dataset_path)

    U = df.drop(columns=['price'])
    v = df['price']

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(U, v, test_size=0.2, random_state=42)

    print("Processando features...")
    pipeline = CarFeaturePipeline()
    X_train, feature_names = pipeline.fit_transform(pd.concat([X_train_raw, y_train], axis=1))
    X_test = pipeline.transform(X_test_raw)

    print("Treinando Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    y_prod = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_prod)
    rmse = np.sqrt(mean_squared_error(y_test, y_prod))
    r2 = r2_score(y_test, y_prod)

    print("\n================= Métricas do Modelo ==================")
    print(f"MAE (Error Médio Absoluto) : R$ {mae:,.2f}")
    print(f"RMSE (Raiz do Erro Quadratico): R$ {rmse:,.2f}")
    print(f"R²   (Coeficiente Det.)    : {r2:.4f}")

    model_path = models_dir / "car_price_model.pkl"
    pipeline_path = models_dir / "feature_pipeline.pkl"

    joblib.dump(model, model_path)
    joblib.dump(pipeline, pipeline_path)

    print(f"Modelo salvo em: {model_path}")
    print(f"Pipeline salva em: {pipeline_path}")

if __name__ == "__main__":
    train_model()

