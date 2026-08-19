import pandas as pd
import numpy as np

REQUIRED_FEATURES = [
    'year', 'engine_cc', 'mileage_km', 'doors',
    'fuel_type', 'transmission', 'body_type', 'state', 'price'
]

def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica limpeza e transformacoes basicas no DataFrame de veiculos."""
    
    # 2. Tratar valores ausentes sem inplace=True
    res = res.dropna(subset=['price'])
    
    if 'mileage_km' in res.columns:
        median_mileage = res['mileage_km'].median()
        res['mileage_km'] = res['mileage_km'].fillna(median_mileage)
        
    if 'engine_cc' in res.columns:
        res['engine_cc'] = res['engine_cc'].fillna(1600)
    
    # 3. Remover outliers extremos de preco
    res = res[(res['price'] > 5000) & (res['price'] < 1000000)]
    
    # 4. Normalizar strings
    for col in ['fuel_type', 'transmission', 'body_type', 'state']:
        if col in res.columns:
            res[col] = res[col].astype(str).str.lower().str.strip()
            
    return res

if __name__ == "__main__":
    print("Módulo prepare_dataset.py carregado e corrigido com sucesso.")
