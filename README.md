# F1 Visualizer

Structure cible du projet final.

```text
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   └── processed/
│       └── telemetry.parquet
├── src/
│   ├── pipeline_fastf1.py
│   ├── data_loader.py
│   └── visualizer.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Roles prevus

- `app/streamlit_app.py` : dashboard web Streamlit.
- `data/raw/` : donnees brutes FastF1 si besoin.
- `data/processed/` : donnees propres pretes a etre lues par l'application.
- `src/pipeline_fastf1.py` : ETL FastF1.
- `src/data_loader.py` : chargement leger des donnees preparees.
- `src/visualizer.py` : fonctions Plotly.
