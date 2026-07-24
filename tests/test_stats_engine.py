import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "Project"))

from stats_engine import StatsEngine


def test_calculate_metrics_returns_none_for_empty_results():
    assert StatsEngine.calculate_metrics([]) is None


def test_calculate_metrics_returns_expected_values():
    results = [{"score": 1}, {"score": 3}, {"score": 2}]

    metrics = StatsEngine.calculate_metrics(results)

    assert metrics["Total Attempts"] == 3
    assert metrics["Average Score"] == pytest.approx(2.0)
    assert metrics["Max Score"] == 3
    assert metrics["Min Score"] == 1
    assert metrics["Median Score"] == pytest.approx(2.0)
    assert metrics["Standard Deviation"] == pytest.approx(0.8164965809)
    assert metrics["Pass Percentage"] == pytest.approx(66.6666666667)
