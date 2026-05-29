# Fonctions Plotly pour les visualisations.
import plotly.graph_objects as go
import pandas as pd
import fastf1.plotting


def create_visualization(data: pd.DataFrame) -> go.Figure:
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

    init_drivers_traces(fig, data)
    manage_buttons(fig)
    
    return fig


def init_drivers_traces(fig: go.Figure, data: pd.DataFrame):
    drivers = data["Driver"].unique()
    for driver in drivers:
        driver_data = data[data["Driver"] == driver]
        driver_team = driver_data["Team"].iloc[0]
        try:
            driver_color = fastf1.plotting.team_color(driver_team)
        except:
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