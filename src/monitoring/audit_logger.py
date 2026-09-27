import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOG_FILE = Path("logs/audit.jsonl")


def log_event(
    event_type: str,
    details: dict[str, Any],
) -> None:
    """Record a pipeline event in the audit log."""

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "details": details,
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")
