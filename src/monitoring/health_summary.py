import json
from pathlib import Path


LOG_FILE = Path("logs/audit.jsonl")


def load_audit_events() -> list[dict]:
    """Load all audit events from the JSONL audit log."""

    if not LOG_FILE.exists():
        return []

    events = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            events.append(json.loads(line))

    return events


def build_health_summary() -> dict:
    """Build a high-level health summary from audit events."""

    events = load_audit_events()

    summary = {
        "total_events": len(events),
        "successful_repairs": 0,
        "rollbacks": 0,
        "review_required": 0,
        "pipeline_success": 0,
    }

    for event in events:
        event_type = event.get("event_type")

        if event_type == "REPAIR_SUCCESS":
            summary["successful_repairs"] += 1

        elif event_type == "ROLLBACK":
            summary["rollbacks"] += 1

        elif event_type == "REVIEW_REQUIRED":
            summary["review_required"] += 1

        elif event_type == "PIPELINE_SUCCESS":
            summary["pipeline_success"] += 1

    return summary
