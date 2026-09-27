from collections import Counter

from src.monitoring.health_summary import load_audit_events


def get_risk_counts() -> dict[str, int]:
    """Return the number of audit events for each risk level."""

    events = load_audit_events()

    counts = Counter()

    for event in events:
        details = event.get("details", {})
        risk_level = details.get("risk_level")

        if risk_level:
            counts[risk_level] += 1

    return dict(counts)
