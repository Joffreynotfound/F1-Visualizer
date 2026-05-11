# MVP - F1 Visualizer

Ce dossier contient le MVP du projet **F1 Visualizer**.

L'objectif principal est d'abord de réaliser une **analyse exploratoire des donnees** afin de mieux comprendre les informations disponibles : pilotes, tours, chronos, telemetrie, vitesse et donnees de circuit.

Une fois cette premiere analyse effectuee, le MVP doit permettre de construire une visualisation simple autour du meilleur tour d'un pilote.

## Objectifs du MVP

1. Explorer les donnees disponibles.
2. Identifier les donnees utiles pour une analyse de performance.
3. Nettoyer et preparer les donnees de telemetrie.
4. Selectionner une course, un pilote ou une session pertinente.
5. Recuperer son meilleur tour.
6. Afficher le trace du circuit.
7. Afficher la vitesse sur le circuit.
8. Afficher quelques metriques simples.

## Fonctionnalites attendues

Le MVP doit permettre de :

- charger les donnees de course et de telemetrie ;
- trouver le meilleur tour d'un pilote ;
- afficher le circuit sous forme de trace ;
- colorer ou annoter le trace avec la vitesse ;
- afficher des metriques simples comme le temps au tour, la vitesse maximale, la vitesse moyenne ou le nombre de points de telemetrie.

## Structure du projet

```text
MVP/
├── app/
│   └── streamlit_app.py
├── data/
├── notebooks/
├── src/
│   ├── data_loader.py
│   ├── telemetry_cleaner.py
│   └── visualizer.py
├── requirements.txt
└── README.md
```

## Prochaine etape

La prochaine etape est de commencer par l'analyse exploratoire dans un notebook, puis de transformer les parties utiles en fonctions reutilisables dans `src/` avant de les afficher dans l'application Streamlit.
