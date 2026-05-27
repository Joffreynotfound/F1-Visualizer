import streamlit as st
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from data_loader import load_data
from visualizer import create_visualization


st.title("F1 Visualizer")

data = load_data(PROJECT_ROOT / "data/processed/lec_telemetry.csv")
if data is None:
    st.write("Failed to load data.")
else:
    fig = create_visualization(data)
    st.metric("Max speed", f"{data['Speed'].max():.0f} km/h")
    st.metric("Average speed", f"{data['Speed'].mean():.0f} km/h")
    st.metric("Telemetry points", len(data))
    st.plotly_chart(fig, use_container_width=True)
