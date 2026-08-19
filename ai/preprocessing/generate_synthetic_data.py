import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import numpy as np
import pandas as pd
from ai.preprocessing.prepare_dataset import clean_and_transform

def generate_cars_data(n_samples: int = 1000, random_seed: int = 42) -> pd.DataFrame:
    np.random.seed(random_seed)
    
    makes = ['Toyota', 'Honda', 'Volkswagen', 'Chevrolet', 'Ford', 'BMW', 'Hyundai']
    fuel_types = ['flex', 'gasolina', 'diesel', 'eletrico', 'hibrido']
    transmissions = ['manual', 'automatico']
    body_types = ['hatch', 'sedan', 'suv', 'picape']
    states = ['SP', 'RJ', 'MG', 'PR', 'RS', 'BA', 'PE']
    
    years = np.random.randint(2010, 2026, size=n_samples)
    
    current_year = 2026
    age = current_year - years
    mileages = np.maximum(0, age * 12000 + np.random.normal(0, 15000, size=n_samples)).astype(int)
    
    engine_ccs = np.random.choice([1000, 1400, 1600, 2000, 3000], size=n_samples, p=[0.3, 0.25, 0.25, 0.15, 0.05])
    doors_list = np.random.choice([2, 4], size=n_samples, p=[0.1, 0.9])
    
    selected_makes = np.random.choice(makes, size=n_samples)
    selected_fuels = np.random.choice(fuel_types, size=n_samples, p=[0.6, 0.2, 0.1, 0.05, 0.05])
    selected_transmissions = np.random.choice(transmissions, size=n_samples, p=[0.4, 0.6])
    selected_bodies = np.random.choice(body_types, size=n_samples, p=[0.3, 0.3, 0.3, 0.1])
    selected_states = np.random.choice(states, size=n_samples)
    
    base_price = 30000
    price = (
        base_price
        + (years - 2010) * 4500
        + (engine_ccs / 100) * 1200
        - (mileages / 10000) * 1500
        + np.where(selected_transmissions == 'automatico', 8000, 0)
        + np.where(selected_makes == 'BMW', 35000, 0)
        + np.random.normal(0, 5000, size=n_samples)
    )
    
    prices = np.maximum(12000, price).round(2)
    
    return pd.DataFrame({
        'make': selected_makes,
        'year': years,
        'engine_cc': engine_ccs,
        'mileage_km': mileages,
        'doors': doors_list,
        'fuel_type': selected_fuels,
        'transmission': selected_transmissions,
        'body_type': selected_bodies,
        'state': selected_states,
        'price': prices
    })

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "datasets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "cars_dataset.csv"
    
    df_raw = generate_cars_data(n_samples=1500)
    df_clean = clean_and_transform(df_raw)
    df_clean.to_csv(out_file, index=False)
    
    print("Dataset sintetico gerado com sucesso!")
    print(f" Salvo em: {out_file}")
    print(f" Registros: {len(df_clean)} linhas, {len(df_clean.columns)} colunas")
