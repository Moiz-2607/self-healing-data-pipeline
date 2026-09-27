import json

from src.monitoring.audit_logger import log_event


def test_log_event(tmp_path, monkeypatch):
    log_file = tmp_path / "audit.jsonl"

    monkeypatch.setattr(
        "src.monitoring.audit_logger.LOG_FILE",
        log_file,
    )

    log_event(
        "REPAIR",
        {
            "column": "age",
            "from": "str",
            "to": "int64",
            "status": "success",
        },
    )

    assert log_file.exists()

    with log_file.open("r", encoding="utf-8") as file:
        event = json.loads(file.readline())

    assert event["event_type"] == "REPAIR"
    assert event["details"]["column"] == "age"
    assert event["details"]["status"] == "success"
    assert "timestamp" in event
