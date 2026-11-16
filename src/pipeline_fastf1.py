# ETL FastF1: extraction, nettoyage et export des donnees.

import fastf1
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = PROJECT_ROOT / "data" / "raw" / "fastf1_cache"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def extract_data(year: int, grand_prix: str, session_type: str) -> pd.DataFrame:
    # Extraction des donnees de la session specifiée
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(CACHE_DIR))
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()  # Charge les donnees de la session
    try:
        session.laps  # leve DataNotLoadedError si le chargement a echoue silencieusement
    except Exception as exc:
        raise RuntimeError(
            f"Chargement impossible des tours pour {year} {grand_prix} {session_type}. "
            "Verifiez le reseau ou l'acces aux donnees F1 (authentification possible selon la version de FastF1)."
        ) from exc

    # Extraction de la liste des pilotes
    drivers = session.results["Abbreviation"].unique().tolist()
    # Extraction des donnees de telemetrie pour chaque pilote
    telemetry_list = []
    for driver in drivers:
        laps = session.laps.pick_drivers(driver)
        fastest_lap = laps.pick_fastest()
        if fastest_lap is None:  # aucun tour valide (abandon, non-partant...)
            continue
        telemetry = fastest_lap.get_telemetry()
        telemetry["Driver"] = driver  # Ajout du nom du pilote dans les donnees
        telemetry["Team"] = session.results.loc[session.results["Abbreviation"] == driver, "TeamName"].values[0]  # Ajout du nom de l'equipe
        color_hex = session.results.loc[session.results["Abbreviation"] == driver, "TeamColor"].values[0]
        telemetry["Color"] = f"#{color_hex}"
        telemetry_list.append(telemetry)

    if not telemetry_list:
        raise RuntimeError(f"Aucune telemetrie exploitable pour {year} {grand_prix} {session_type}.")
    telemetry = pd.concat(telemetry_list, ignore_index=True)
    telemetry.to_parquet(PROCESSED_DIR / f"{year}_{grand_prix}_{session_type}_telemetry.parquet", index=False)
    return telemetry
