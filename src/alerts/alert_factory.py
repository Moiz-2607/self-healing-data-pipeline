import os

from dotenv import load_dotenv

load_dotenv()

from src.alerts.alert_manager import AlertManager
from src.alerts.console_alert import ConsoleAlertManager
from src.alerts.slack_alert import SlackAlertManager


def get_alert_manager() -> AlertManager:
    provider = os.getenv("ALERT_PROVIDER", "console").lower()

    if provider == "console":
        return ConsoleAlertManager()

    if provider == "slack":
        webhook_url = os.getenv("SLACK_WEBHOOK_URL", "")
        return SlackAlertManager(webhook_url)

    raise ValueError(f"Unsupported alert provider: {provider}")
