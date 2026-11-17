from src.visualizer import create_telemetry_chart, create_visualization


def test_map_has_track_drivers_and_frames(make_session):
    data = make_session(["LEC", "VER"])
    fig = create_visualization(data, ["LEC", "VER"], "Classique (Gris)")
    assert len(fig.data) == 3  # trace du circuit + 2 pilotes
    assert len(fig.frames) == len(data[data["Driver"] == "LEC"])


def test_thermal_mode_colors_track_by_speed(make_session):
    fig = create_visualization(make_session(["LEC"]), ["LEC"], "Thermique (Vitesse)")
    assert fig.data[0].marker.color is not None


def test_telemetry_chart_one_line_per_driver(make_session):
    fig = create_telemetry_chart(make_session(["LEC", "HAM"]), ["LEC", "HAM"], "Speed")
    assert [t.name for t in fig.data] == ["LEC", "HAM"]


def test_missing_color_column_falls_back(make_session):
    data = make_session(["LEC"]).drop(columns=["Color"])
    fig = create_telemetry_chart(data, ["LEC"], "Speed")
    assert fig.data[0].line.color == "#FFFFFF"
