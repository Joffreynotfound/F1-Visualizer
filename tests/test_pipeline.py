from unittest import mock

import pandas as pd
import pytest

import src.pipeline_fastf1 as pl


@pytest.fixture
def dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(pl, "CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(pl, "PROCESSED_DIR", tmp_path / "processed")
    return tmp_path


def _fake_session(results, telemetry_by_driver):
    """Session FastF1 factice : aucune requete reseau."""
    session = mock.MagicMock()
    session.results = pd.DataFrame(results)

    def pick_drivers(driver):
        laps = mock.MagicMock()
        tel = telemetry_by_driver[driver]
        laps.pick_fastest.return_value = None if tel is None else mock.MagicMock(
            get_telemetry=mock.MagicMock(return_value=tel.copy()))
        return laps

    session.laps.pick_drivers.side_effect = pick_drivers
    return session


RESULTS = [
    {"Abbreviation": "LEC", "TeamName": "Ferrari", "TeamColor": "E8002D"},
    {"Abbreviation": "XXX", "TeamName": "Test", "TeamColor": "FFFFFF"},
]


def test_laps_not_loaded_gives_clear_error(dirs):
    fake = mock.MagicMock()
    type(fake).laps = mock.PropertyMock(side_effect=RuntimeError("not loaded"))
    with mock.patch.object(pl.fastf1, "get_session", return_value=fake), \
            mock.patch.object(pl.fastf1.Cache, "enable_cache"):
        with pytest.raises(RuntimeError, match="Chargement impossible des tours"):
            pl.extract_data(2023, "Monza", "R")


def test_driver_without_valid_lap_is_skipped_and_dirs_created(dirs, real_lap):
    session = _fake_session(RESULTS, {"LEC": real_lap, "XXX": None})
    with mock.patch.object(pl.fastf1, "get_session", return_value=session), \
            mock.patch.object(pl.fastf1.Cache, "enable_cache"):
        df = pl.extract_data(2023, "Monza", "R")
    assert set(df["Driver"]) == {"LEC"}
    assert df["Color"].iloc[0] == "#E8002D"
    assert (dirs / "processed" / "2023_Monza_R_telemetry.parquet").exists()


def test_no_usable_telemetry_raises(dirs):
    session = _fake_session(RESULTS, {"LEC": None, "XXX": None})
    with mock.patch.object(pl.fastf1, "get_session", return_value=session), \
            mock.patch.object(pl.fastf1.Cache, "enable_cache"):
        with pytest.raises(RuntimeError, match="Aucune telemetrie"):
            pl.extract_data(2023, "Monza", "R")
