from collections import Counter

from src.monitoring.health_summary import load_audit_events


def get_event_counts() -> dict[str, int]:
    """Return the number of occurrences for each audit event type."""

    events = load_audit_events()

    counts = Counter(
        event.get("event_type", "UNKNOWN")
        for event in events
    )

    return dict(counts)
