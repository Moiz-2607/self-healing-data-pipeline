from src.monitoring.health_summary import build_health_summary


def test_health_summary_contains_expected_fields():
    summary = build_health_summary()

    assert "total_events" in summary
    assert "successful_repairs" in summary
    assert "rollbacks" in summary
    assert "review_required" in summary
    assert "pipeline_success" in summary


def test_health_summary_values_are_non_negative():
    summary = build_health_summary()

    for value in summary.values():
        assert isinstance(value, int)
        assert value >= 0


def test_health_summary_counts_are_consistent():
    summary = build_health_summary()

    counted_events = (
        summary["successful_repairs"]
        + summary["rollbacks"]
        + summary["review_required"]
        + summary["pipeline_success"]
    )

    assert counted_events == summary["total_events"]
