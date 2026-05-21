import pandas as pd
import plotly.express as px

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None

def generate_map(data):
    fig = px.scatter(
        data,
        x="X",
        y="Y",
        color="Speed",
        size="Speed",
        title="F1 Telemetry Map"
    )
    return fig

