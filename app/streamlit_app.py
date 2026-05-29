# Dashboard Streamlit.

from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_data
from src.visualizer import create_visualization
from src.pipeline_fastf1 import extract_data

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="F1 Telemetry Visualizer", layout="wide")

def main():
    st.title("F1 Telemetry Visualizer")
    st.markdown("Visualisez les données de télémétrie des pilotes de Formule 1 en temps réel.")

    # Sélection de la session
    year = st.sidebar.selectbox("Année", [2023, 2022, 2021])
    grand_prix = st.sidebar.selectbox("Grand Prix", ["Monaco", "Silverstone", "Monza"])
    session_type = st.sidebar.selectbox("Type de session", ["Q", "R"])

    # Extraction des données
    extract_data(year, grand_prix, session_type)
    
    # Chargement des données
    file_path = PROCESSED_DATA_DIR / f"{year}_{grand_prix}_{session_type}_telemetry.parquet"
    data = load_data(str(file_path))

    if data is not None:
        fig = create_visualization(data)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Impossible de charger les données. Veuillez vérifier le chemin d'accès et le format du fichier.")


if __name__ == "__main__":
    main()
