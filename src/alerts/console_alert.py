from typing import Any

from src.alerts.alert_manager import AlertManager


class ConsoleAlertManager(AlertManager):
    """Print alerts to the terminal."""

    def send_alert(
        self,
        alert_type: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        print()
        print("=" * 58)
        print("PIPELINE ALERT")
        print("=" * 58)
        print(f"Type:    {alert_type}")
        print(f"Message: {message}")

        if details:
            print("Details:")
            for key, value in details.items():
                print(f"  {key}: {value}")

        print("=" * 58)
