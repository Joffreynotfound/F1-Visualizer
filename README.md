# F1 Telemetry Visualizer

Visualiseur open source de télémétrie Formula 1 construit avec FastF1, Streamlit et Plotly.

Le projet permet d'extraire les données publiques FastF1, de les transformer en fichiers Parquet locaux, puis de comparer les pilotes sur une interface interactive : trajectoire sur le circuit, animation, vitesse maximale et courbes de télémétrie.

## Objectif

F1 Telemetry Visualizer vise à rendre l'analyse de télémétrie F1 plus accessible, reproductible et améliorable par la communauté.

Le projet est pensé comme une base open source simple à comprendre :

- une pipeline d'extraction claire avec FastF1;
- des fichiers de données traitées au format Parquet;
- une application Streamlit légère;
- des visualisations Plotly isolées dans `src/visualizer.py`;
- une architecture volontairement modulaire pour faciliter les contributions.

## Fonctionnalités

- Extraction des données depuis FastF1 pour une année, un Grand Prix et un type de session.
- Cache local FastF1 dans `data/raw/fastf1_cache`.
- Export des télémétries traitées dans `data/processed`.
- Chargement des fichiers Parquet depuis l'application Streamlit.
- Sélection de pilotes à comparer.
- Affichage du tracé du circuit en mode classique ou thermique.
- Animation des positions sur le circuit.
- Comparaison de métriques comme `Speed`, `Throttle`, `Brake` et `nGear`.

## Installation

Clonez le projet, puis créez un environnement virtuel :

```bash
git clone https://github.com/Joffreynotfound/F1-Visualizer.git
cd F1-Visualizer
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Lancer l'application

```bash
streamlit run app/streamlit_app.py
```

Au premier lancement d'une session non disponible localement, l'application propose d'extraire les données depuis FastF1. Les fichiers générés sont ensuite réutilisés depuis `data/processed`.

## Structure

```text
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   │   └── fastf1_cache/
│   └── processed/
├── src/
│   ├── pipeline_fastf1.py
│   ├── data_loader.py
│   └── visualizer.py
├── requirements.txt
└── README.md
```

## Rôles des fichiers

- `app/streamlit_app.py` : interface Streamlit et orchestration de l'expérience utilisateur.
- `src/pipeline_fastf1.py` : extraction FastF1, enrichissement des données et export Parquet.
- `src/data_loader.py` : chargement et validation minimale des fichiers préparés.
- `src/visualizer.py` : construction des graphiques Plotly.
- `data/raw/` : cache local et données brutes.
- `data/processed/` : données nettoyées prêtes à être affichées.

## Données

Les données proviennent de FastF1. Elles ne sont pas destinées à être versionnées dans Git si elles sont volumineuses ou générées localement.

Le format de sortie attendu est :

```text
data/processed/{year}_{grand_prix}_{session_type}_telemetry.parquet
```

Exemple :

```text
data/processed/2023_Monaco_Q_telemetry.parquet
```

## Contribuer

Les contributions sont bienvenues. L'objectif est de garder le projet accessible aux personnes qui découvrent Python, Streamlit, la data visualisation ou l'analyse F1.

Idées de contributions utiles :

- ajouter de nouveaux circuits ou presets de sessions;
- améliorer l'ergonomie de l'interface Streamlit;
- ajouter des graphiques de télémétrie;
- comparer les mini-secteurs ou les temps intermédiaires;
- améliorer la robustesse de la pipeline FastF1;
- ajouter des tests sur le chargement et la validation des données;
- documenter les limites connues et les cas d'usage.

Avant de proposer une modification :

1. Créez une branche dédiée.
2. Gardez les changements ciblés.
3. Vérifiez que l'application démarre.
4. Décrivez clairement le problème résolu ou l'amélioration apportée.

## Principes open source

Ce projet cherche à privilégier :

- la lisibilité du code plutôt que les abstractions prématurées;
- des modules simples et testables;
- des formats ouverts et réutilisables;
- une documentation utile pour les nouveaux contributeurs;
- des contributions progressives, même petites.

Les issues, suggestions et pull requests sont encouragées. Une contribution n'a pas besoin d'être massive pour être utile : correction de documentation, nettoyage de code, ajout d'un exemple ou amélioration d'un message d'erreur sont aussi des apports importants.

## Feuille de route

- Ajouter un fichier `CONTRIBUTING.md`.
- Ajouter une licence open source explicite.
- Ajouter des tests unitaires.
- Ajouter une gestion plus fine des erreurs FastF1.
- Ajouter une sélection plus flexible des saisons, Grands Prix et sessions.
- Améliorer l'animation et la synchronisation des pilotes.
- Ajouter des exports de graphiques ou de données filtrées.

## 📄 Licence

Ce projet est distribué sous la licence MIT. Voir le fichier `LICENSE` pour plus d'informations.
