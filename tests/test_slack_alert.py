import json

from src.alerts.slack_alert import SlackAlertManager


class FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def test_slack_alert_sends_expected_payload(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse()

    monkeypatch.setattr(
        "src.alerts.slack_alert.urllib.request.urlopen",
        fake_urlopen,
    )

    manager = SlackAlertManager("https://example.com/webhook")

    manager.send_alert(
        "HUMAN_REVIEW",
        "Required column is missing.",
        {"risk_level": "HIGH"},
    )

    assert captured["url"] == "https://example.com/webhook"
    assert captured["timeout"] == 10
    assert "Pipeline Alert" in captured["body"]["text"]
    assert "HUMAN_REVIEW" in captured["body"]["text"]
    assert "Required column is missing." in captured["body"]["text"]
    assert "HIGH" in captured["body"]["text"]
