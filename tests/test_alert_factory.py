import pytest

from src.alerts.alert_factory import get_alert_manager
from src.alerts.console_alert import ConsoleAlertManager


def test_alert_factory_defaults_to_console(monkeypatch):
    monkeypatch.delenv("ALERT_PROVIDER", raising=False)

    manager = get_alert_manager()

    assert isinstance(manager, ConsoleAlertManager)


def test_alert_factory_rejects_unsupported_provider(monkeypatch):
    monkeypatch.setenv("ALERT_PROVIDER", "unknown")

    with pytest.raises(ValueError, match="Unsupported alert provider"):
        get_alert_manager()
