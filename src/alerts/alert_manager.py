from typing import Any


class AlertManager:
    """Base alert manager for pipeline events."""

    def send_alert(
        self,
        alert_type: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        raise NotImplementedError
