from src.monitoring.health_summary import load_audit_events


def get_recent_events(limit: int = 10) -> list[dict]:
    """Return the most recent audit events."""

    events = load_audit_events()

    return events[-limit:][::-1]
