import plotly.graph_objects as go
import pandas as pd


def create_visualization(data: pd.DataFrame, driver_name: str = "Leclerc", driver_color: str = "rgba(255, 0, 0, 1)") -> go.Figure:
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
            marker=dict(color=driver_color, size=14, symbol="circle"),
            name=driver_name,
            hoverinfo="skip"
            )
    )
    # Chaque frame met a jour uniquement la trace 1, c'est-a-dire le marqueur
    # du pilote. La trace 0 correspond au circuit et reste fixe.
    frames = [
        go.Frame(
            data=[go.Scatter(x=[row["X"]], y=[row["Y"]])],
            name=f"frame_{i}",
            traces=[1]
        )
        for i, row in data.iterrows()
    ]
    fig.frames = frames
    
    manage_buttons(fig)

    return fig


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
