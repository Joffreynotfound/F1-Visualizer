# MVP - F1 Visualizer

Ce dossier contient le MVP du projet **F1 Visualizer**.

L'application Streamlit affiche la telemetrie du meilleur tour de Charles Leclerc a Monza. Elle s'appuie sur un CSV deja prepare dans `data/processed/lec_telemetry.csv`, puis affiche le trace du circuit, un marqueur anime pour le pilote et quelques metriques simples.

## Fonctionnalites actuelles

- Chargement d'un fichier CSV de telemetrie propre.
- Validation des colonnes minimales attendues : `X`, `Y`, `Speed`, `Time`.
- Visualisation du trace du circuit avec Plotly.
- Animation du pilote sur la carte a partir des coordonnees `X` et `Y`.
- Selection de la couleur du pilote dans l'interface Streamlit.
- Affichage de metriques simples :
  - vitesse maximale ;
  - vitesse moyenne ;
  - nombre de points de telemetrie.

## Structure

```text
MVP/
├── app/
│   └── streamlit_app.py
├── data/
│   └── processed/
│       └── lec_telemetry.csv
├── notebooks/
│   └── EDA_Fastf1.ipynb
├── src/
│   ├── data_loader.py
│   └── visualizer.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Roles des fichiers

- `app/streamlit_app.py` : point d'entree de l'application Streamlit.
- `src/data_loader.py` : charge le CSV et verifie que les colonnes necessaires sont presentes.
- `src/visualizer.py` : construit la figure Plotly, le trace du circuit, le pilote et les boutons Play/Pause.
- `notebooks/EDA_Fastf1.ipynb` : notebook d'exploration FastF1 utilise pour analyser les donnees et exporter le CSV propre.
- `data/processed/lec_telemetry.csv` : donnees de telemetrie utilisees par l'application.

## Lancer l'application

Depuis la racine du repository :

```bash
cd MVP
source env/bin/activate
streamlit run app/streamlit_app.py
```

Si les dependances ne sont pas encore installees :

```bash
cd MVP
source env/bin/activate
pip install -r requirements.txt
```

## Pipeline actuel

```text
Notebook FastF1
    ↓
Nettoyage et export CSV
    ↓
data/processed/lec_telemetry.csv
    ↓
Application Streamlit
    ↓
Carte animee + metriques
```

Le nettoyage n'est pas refait dans l'application. Le MVP part du principe que le fichier `lec_telemetry.csv` est deja propre.

## Ameliorations possibles

- Ajouter un choix de pilote ou de course.
- Ajouter un slider pour regler la vitesse de l'animation.
- Afficher la vitesse avec une couleur sur le trace.
- Ajouter des graphiques vitesse, throttle et freinage en fonction de la distance.
- Deplacer la generation du CSV dans un script reproductible si l'application doit charger des donnees FastF1 dynamiquement.
