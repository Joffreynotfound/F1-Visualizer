# Chargement leger des donnees preparees pour Streamlit.

import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"X", "Y", "Speed", "Time", "Driver", "Team"}


def validate_telemetry_data(data: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Colonnes manquantes : {sorted(missing_columns)}")


def load_data(file_path: str) -> pd.DataFrame:
    """Charge et valide un fichier Parquet. Leve une exception en cas de probleme."""
    data = pd.read_parquet(file_path)
    validate_telemetry_data(data)
    logger.info("Donnees chargees depuis %s", file_path)
    return data
