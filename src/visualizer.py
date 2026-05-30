# Fonctions Plotly pour les visualisations.
import plotly.graph_objects as go
import pandas as pd
import fastf1.plotting


def create_visualization(data: pd.DataFrame, selected_drivers: list, track_mode: str) -> go.Figure:
    fig = go.Figure()

    ref_driver = data["Driver"].unique()[0]
    ref_data = data[data["Driver"] == ref_driver]

    if track_mode == "Thermique (Vitesse)":
        fig.add_trace(
            go.Scatter(
                x=ref_data["X"],
                y=ref_data["Y"],
                mode="markers", # On utilise des points
                marker=dict(
                    color=ref_data["Speed"],
                    colorscale="Turbo",      
                    cmin=50,               
                    cmax=330,               
                    size=6,                  
                    showscale=False,         
                    opacity=0.8               
                ),
                name="Track Speed",
                hoverinfo="skip"
            )
        )
    if track_mode == "Classique (Gris)":
      fig.add_trace(
        go.Scatter(
            x=ref_data["X"],
            y=ref_data["Y"],
            mode="lines",
            line=dict(
                color="rgba(180, 180, 180, 0.35)",
                width=8
            ),
            name="Track layout",
            hoverinfo="skip"
        )
    )
    init_drivers_traces(fig, data, selected_drivers)
    create_animation(fig, data, selected_drivers)
    manage_buttons(fig)

    return fig

def create_animation(fig: go.Figure, data : pd.DataFrame, selected_drivers: list):
        all_frames = []
        max_points = data.groupby("Driver").size().max()
        for i in range(max_points):
            frame_data = []
            traces_to_update = []
            for j, driver in enumerate(selected_drivers):
                driver_data = data[data["Driver"] == driver]
                driver_points = len(driver_data)
                if i < driver_points:
                    xi = driver_data["X"].iloc[i]
                    yi = driver_data["Y"].iloc[i]
                else:
                    xi = driver_data["X"].iloc[-1]
                    yi = driver_data["Y"].iloc[-1]
                frame_data.append(go.Scatter(x=[xi], y=[yi]))
                traces_to_update.append(j + 1)
            frame = go.Frame(
                data=frame_data,
                name=f"frame_{i}",
                traces=traces_to_update
            )
            all_frames.append(frame)
        
        fig.frames = all_frames


def init_drivers_traces(fig: go.Figure, data: pd.DataFrame, selected_drivers: list):
    for driver in selected_drivers:
        driver_data = data[data["Driver"] == driver]
        driver_team = driver_data["Team"].iloc[0]
        try:
            driver_color = driver_data["Color"].iloc[0]
        except:
            print(f"Warning: No color found for team '{driver_team}'. Using default color.")
            driver_color = "#FFFFFF"
        fig.add_trace(
            go.Scatter(
                x=[driver_data["X"].iloc[0]],
                y=[driver_data["Y"].iloc[0]],
                mode="markers",
                marker=dict(color=driver_color, size=14, symbol="circle"),
                name=driver,
                hoverinfo="skip"
            )
        )

def manage_buttons(fig: go.Figure):
    # Les boutons Plotly declenchent les frames definies dans `fig.frames`.
    fig.update_layout(
        template="plotly_dark",
        height=750,
        showlegend=False,
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis=dict(visible=False, scaleanchor="y"),
        yaxis=dict(visible=False),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            direction="right",
            x=0.0,
            y=1.1,
            xanchor="left",
            yanchor="top",
            pad=dict(r=10, t=0),
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

def create_telemetry_chart(data: pd.DataFrame, selected_drivers: list, metric: str) -> go.Figure:
    fig = go.Figure()
    
    for driver in selected_drivers:
        driver_data = data[data["Driver"] == driver]
        
        try:
            driver_color = driver_data["Color"].iloc[0]
        except:
            driver_color = "#FFFFFF"

        fig.add_trace(go.Scatter(
            x=driver_data["Distance"],
            y=driver_data[metric],
            mode="lines",
            name=driver,
            line=dict(color=driver_color, width=2)
        ))
        
    fig.update_layout(
        template="plotly_dark",
        height=350, # Moins haut que la carte
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis_title="Distance parcourue (m)",
        yaxis_title=metric,
        legend=dict(
            orientation="h", # Légende horizontale
            yanchor="bottom", y=1.02, 
            xanchor="right", x=1
        )
    )
    
    return fig