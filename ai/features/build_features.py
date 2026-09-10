import sys
from pathlib import Path

# Garantir imports do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

NUMERICAL_FEATURES = ['year', 'engine_cc', 'mileage_km', 'doors', 'vehicle_age', 'km_per_year']
CATEGORICAL_FEATURES = ['make', 'fuel_type', 'transmission', 'body_type', 'state']

class CarFeaturePipeline:
    """Pipeline de engenharia de recursos para o modelo de precificacao de veiculos."""
    
    def __init__(self):
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), NUMERICAL_FEATURES),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES)
            ],
            remainder='drop'
        )
        self.is_fitted = False

    def fit_transform(self, df: pd.DataFrame):
        """Ajusta os transformadores e converte os dados em uma matriz pronta para ML."""
        df = df.copy()
        df['vehicle_age'] = 2025 - df['year']
        df['km_per_year'] = df['mileage_km'] / df['vehicle_age'].clip(lower=1)
        X = df.drop(columns=['price'], errors='ignore')
        X_trans = self.preprocessor.fit_transform(X)
        self.is_fitted = True
        
        # Recuperar nomes das colunas apos OneHotEncoding
        cat_encoder = self.preprocessor.named_transformers_['cat']
        cat_cols = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
        feature_names = NUMERICAL_FEATURES + cat_cols
        
        return X_trans, feature_names

    def transform(self, df: pd.DataFrame):
        """Aplica as transformacoes em dados novos sem recalcular medias/desvios."""
        if not self.is_fitted:
            raise RuntimeError("O pipeline de features precisa ser ajustado com fit_transform primeiro.")
        df = df.copy()
        df['vehicle_age'] = 2025 - df['year']
        df['km_per_year'] = df['mileage_km'] / df['vehicle_age'].clip(lower=1)
        X = df.drop(columns=['price'], errors='ignore')
        return self.preprocessor.transform(X)

if __name__ == "__main__":
    csv_path = BASE_DIR / "ai" / "datasets" / "cars_dataset.csv"
    if not csv_path.exists():
        print(f" Dataset nao encontrado em {csv_path}. Execute o generate_synthetic_data.py primeiro.")
    else:
        df = pd.read_csv(csv_path)
        pipeline = CarFeaturePipeline()
        X_trans, feature_names = pipeline.fit_transform(df)
        
        print("Pipeline de Features construida e validada com sucesso!")
        print(f" Shape do dataset transformado: {X_trans.shape}")
        print(f" Total de features geradas: {len(feature_names)}")
        print(f" Exemplos de features: {feature_names[:6]} ...")
