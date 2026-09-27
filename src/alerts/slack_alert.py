import json
import urllib.request
from typing import Any

from src.alerts.alert_manager import AlertManager


class SlackAlertManager(AlertManager):
    def __init__(self, webhook_url: str):
        if not webhook_url:
            raise ValueError("Slack webhook URL is required.")

        self.webhook_url = webhook_url

    def send_alert(
        self,
        alert_type: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        payload = {
            "text": (
                f"🚨 *Pipeline Alert*\n"
                f"*Type:* {alert_type}\n"
                f"*Message:* {message}\n"
                f"*Details:* {json.dumps(details or {}, default=str)}"
            )
        }

        request = urllib.request.Request(
            self.webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Slack alert failed with status {response.status}."
                )
