import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def generate_map(data):
    fig = go.Figure()

    # Ligne de base du circuit
    fig.add_trace(
        go.Scatter(
            x=data["X"],
            y=data["Y"],
            mode="lines",
            line=dict(
                color="rgba(180, 180, 180, 0.35)",
                width=8
            ),
            name="Track layout",
            hoverinfo="skip"
        )
    )

    fig.update_layout(
        title="Leclerc Fastest Lap — Speed Map",
        template="plotly_dark",
        height=750,
        showlegend=False,
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            visible=False,
            scaleanchor="y"
        ),
        yaxis=dict(
            visible=False
        )
    )

    return fig

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None

st.title("F1 Visualizer")

data = load_data('data/processed/lec_telemetry.csv')
if data is None:
    st.write("Failed to load data.")
else:
    fig = generate_map(data)
    st.plotly_chart(fig, use_container_width=True)