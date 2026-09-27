from src.monitoring.risk_counts import get_risk_counts


def test_risk_counts_returns_dict():
    counts = get_risk_counts()

    assert isinstance(counts, dict)


def test_risk_counts_values_are_non_negative():
    counts = get_risk_counts()

    for value in counts.values():
        assert isinstance(value, int)
        assert value >= 0


def test_risk_counts_only_contains_valid_levels():
    counts = get_risk_counts()

    assert set(counts).issubset(
        {"LOW", "MEDIUM", "HIGH"}
    )
