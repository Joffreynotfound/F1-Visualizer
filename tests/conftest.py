"""Fixtures partagees.

La telemetrie de base est REELLE (meilleur tour de Leclerc, Monza 2022, extrait avec FastF1).
Les jeux a plusieurs pilotes sont SYNTHETIQUES : ils dupliquent ce tour sous d'autres noms,
uniquement pour tester le comportement du code, jamais pour produire des chiffres.
"""
from pathlib import Path

import pandas as pd
import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "lec_monza2022_fastest_lap.csv"


@pytest.fixture(scope="session")
def real_lap() -> pd.DataFrame:
    df = pd.read_csv(FIXTURE)
    df["Time"] = pd.to_timedelta(df["Time"])
    df["SessionTime"] = pd.to_timedelta(df["SessionTime"])
    return df


@pytest.fixture
def make_session(real_lap):
    def _make(drivers):
        parts = []
        for d in drivers:
            x = real_lap.copy()
            x["Driver"], x["Team"], x["Color"] = d, f"Team_{d}", "#FF0000"
            parts.append(x)
        return pd.concat(parts, ignore_index=True)
    return _make
