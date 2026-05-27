import streamlit as st
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

# Streamlit lance ce fichier depuis `app/`, donc on ajoute `src/` au path
# pour pouvoir importer les modules du projet sans installer un package local.
sys.path.append(str(SRC_DIR))

from data_loader import load_data
from visualizer import create_visualization


st.title("F1 Visualizer")

data_path = PROJECT_ROOT / "data/processed/lec_telemetry.csv"
data = load_data(data_path)
if data is None:
    st.write("Failed to load data.")
else:
    driver_color = st.color_picker("Driver color", "#ff0000")
    fig = create_visualization(data, driver_color=driver_color)

    st.metric("Max speed", f"{data['Speed'].max():.0f} km/h")
    st.metric("Average speed", f"{data['Speed'].mean():.0f} km/h")
    st.metric("Telemetry points", len(data))
    st.plotly_chart(fig, use_container_width=True)
