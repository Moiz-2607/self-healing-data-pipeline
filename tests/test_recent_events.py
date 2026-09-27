from src.monitoring.recent_events import get_recent_events


def test_recent_events_returns_list():
    events = get_recent_events()

    assert isinstance(events, list)


def test_recent_events_respects_limit():
    events = get_recent_events(limit=5)

    assert len(events) <= 5


def test_recent_events_are_most_recent_first():
    events = get_recent_events(limit=5)

    if len(events) >= 2:
        assert events[0]["timestamp"] >= events[1]["timestamp"]
