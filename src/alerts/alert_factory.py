from src.alerts.alert_manager import AlertManager
from src.alerts.console_alert import ConsoleAlertManager


def get_alert_manager() -> AlertManager:
    """Return the configured alert manager."""
    return ConsoleAlertManager()
