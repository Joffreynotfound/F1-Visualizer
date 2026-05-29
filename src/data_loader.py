# Chargement leger des donnees preparees pour Streamlit.

import pandas as pd

REQUIRED_COLUMNS = {"X", "Y", "Speed", "Time", "Driver", "Team"}

def validate_telemetry_data(data):
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

def load_data(file_path: str) -> pd.DataFrame:
    try:
        data = pd.read_parquet(file_path)
        validate_telemetry_data(data)
        print(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None
