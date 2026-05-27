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

    # Ajout du pilote
    fig.add_trace(
        go.Scatter(
            x=[data["X"].iloc[0]],
            y=[data["Y"].iloc[0]],
            mode="markers",
            marker=dict(color="rgba(255, 0, 0, 1)", size=14, symbol="circle"),
            name="Leclerc",
            hoverinfo="skip"
        )
    )
    # Lancement de l'usine de calques pour l'animation
    frames = [
        go.Frame(
            data=[go.Scatter(x=[row["X"]], y=[row["Y"]])],
            name=f"frame_{i}",
            traces=[1]  # Met à jour uniquement le pilote
        )
        for i, row in data.iterrows()
    ]
    fig.frames = frames

    # Lecteur de l'animation

    fig.update_layout(
        template="plotly_dark",
        height=750,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(visible=False, scaleanchor="y"),
        yaxis=dict(visible=False),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            y=0, x=0.05,
            xanchor="left", yanchor="bottom",
            buttons=[
                dict(
                    label="🏁 Play",
                    method="animate",
                    args=[None, dict(frame=dict(duration=40, redraw=False), 
                                     transition=dict(duration=0), 
                                     fromcurrent=True)]
                ),
                dict(
                    label="⏸ Pause",
                    method="animate",
                    args=[[None], dict(frame=dict(duration=0, redraw=False), 
                                       mode="immediate", transition=dict(duration=0))]
                )
            ]
        )]
    )
    # frames = []

    # for i, row in data.iterrows():
    #     frame = go.Frame(
    #         data=[go.Scatter(x=[row["X"]], y=[row["Y"]])],
    #         name=f"frame_{i}"
    #     )
    #     frames.append(frame)
    
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