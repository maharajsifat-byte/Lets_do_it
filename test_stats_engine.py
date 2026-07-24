from Project.stats_engine import StatsEngine


def test_calculate_metrics_empty_results_returns_none():
    assert StatsEngine.calculate_metrics([]) is None
