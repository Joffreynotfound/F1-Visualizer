# Dashboard Streamlit.

from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_data
from src.visualizer import create_visualization, create_telemetry_chart
from src.pipeline_fastf1 import extract_data

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="F1 Telemetry Visualizer", layout="wide")

st.title("F1 Telemetry Visualizer")
st.markdown("Visualisez les données de télémétrie des pilotes de Formule 1 en temps réel.")

# Sélection de la session
year = st.sidebar.selectbox("Année", [2023, 2022, 2021])
grand_prix = st.sidebar.selectbox("Grand Prix", ["Monaco", "Silverstone", "Monza"])
session_type = st.sidebar.selectbox("Type de session", ["Q", "R"])

# Chargement des données
file_path = PROCESSED_DATA_DIR / f"{year}_{grand_prix}_{session_type}_telemetry.parquet"

if not file_path.exists():
    st.warning(f"Les données pour {year} {grand_prix} ({session_type}) ne sont pas encore sur votre disque.")
    
    if st.button("Lancer l'extraction des données depuis FastF1"):
        with st.spinner("Téléchargement et traitement des données en cours (peut prendre une minute)..."):
            extract_data(year, grand_prix, session_type)
            st.success("Extraction terminée avec succès !")
            st.rerun()
            
    st.stop()

@st.cache_data
def get_data():
     return load_data(str(file_path))
data = get_data()

if data is not None:
    st.sidebar.header("Contrôle de la Course")
    
    all_drivers = data["Driver"].unique().tolist()
    
    selected_drivers = st.sidebar.multiselect(
        "Sélectionnez les pilotes à comparer :",
        options=all_drivers,
        default=["VER", "LEC"],
        key="selector_pilotes_duel"
    )

    metric_to_plot = st.sidebar.selectbox(
    " Choisissez la télémétrie à analyser :",
    options=["Speed", "Throttle", "Brake", "nGear"], #
    index=0
)
    
    if not selected_drivers:
        st.warning("Veuillez sélectionner au moins un pilote dans le menu de gauche.")
    else:

        track_mode = st.sidebar.radio(
        "Style du circuit :",
        options=["Classique (Gris)", "Thermique (Vitesse)"]
    )
        st.markdown("### 🏎️ Grille de Départ & Top Vitesse")
    
        # On crée dynamiquement autant de colonnes qu'il y a de pilotes sélectionnés
        cols = st.columns(len(selected_drivers))
        
        for index, driver in enumerate(selected_drivers):
            # On extrait les infos du pilote
            driver_data = data[data["Driver"] == driver]
            team_name = driver_data["Team"].iloc[0]
            max_speed = int(driver_data["Speed"].max()) # Vitesse max absolue
            
            # On remplit la colonne correspondante
            with cols[index]:
                # st.metric crée un très beau widget avec un grand chiffre
                st.metric(
                    label=f"{driver} ({team_name})",
                    value=f"{max_speed} km/h"
                )
            
        st.divider()
        st.markdown("### Animation du Circuit")
        fig_map = create_visualization(data, selected_drivers, track_mode)
        st.plotly_chart(fig_map, use_container_width=True)
    
        st.markdown("### Analyse Télémétrique")
        fig_telemetry = create_telemetry_chart(data, selected_drivers, metric_to_plot)
        st.plotly_chart(fig_telemetry, use_container_width=True)
