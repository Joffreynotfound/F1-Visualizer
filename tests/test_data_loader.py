import pytest

from src.data_loader import REQUIRED_COLUMNS, load_data, validate_telemetry_data


def test_valid_file_loads(tmp_path, make_session):
    path = tmp_path / "ok.parquet"
    make_session(["LEC", "VER"]).to_parquet(path, index=False)
    df = load_data(str(path))
    assert REQUIRED_COLUMNS <= set(df.columns)
    assert set(df["Driver"]) == {"LEC", "VER"}


def test_missing_columns_raise_explicit_error(real_lap):
    with pytest.raises(ValueError, match="Colonnes manquantes"):
        validate_telemetry_data(real_lap[["X", "Y"]])


def test_missing_file_raises(tmp_path):
    with pytest.raises(Exception):
        load_data(str(tmp_path / "absent.parquet"))
