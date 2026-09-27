from src.monitoring.event_counts import get_event_counts


def test_event_counts_returns_dict():
    counts = get_event_counts()

    assert isinstance(counts, dict)


def test_event_counts_values_are_non_negative():
    counts = get_event_counts()

    for value in counts.values():
        assert isinstance(value, int)
        assert value >= 0


def test_event_counts_total_matches_audit_events():
    from src.monitoring.health_summary import load_audit_events

    counts = get_event_counts()
    events = load_audit_events()

    assert sum(counts.values()) == len(events)
