from src.alerts.console_alert import ConsoleAlertManager


def test_console_alert_manager(capsys):
    alert_manager = ConsoleAlertManager()

    alert_manager.send_alert(
        "HUMAN_REVIEW",
        "Test alert",
        {
            "risk_level": "HIGH",
            "status": "REVIEW_REQUIRED",
        },
    )

    captured = capsys.readouterr()

    assert "PIPELINE ALERT" in captured.out
    assert "HUMAN_REVIEW" in captured.out
    assert "Test alert" in captured.out
    assert "HIGH" in captured.out
    assert "REVIEW_REQUIRED" in captured.out


def test_console_alert_without_details(capsys):
    alert_manager = ConsoleAlertManager()

    alert_manager.send_alert(
        "ROLLBACK",
        "Rollback occurred.",
    )

    captured = capsys.readouterr()

    assert "PIPELINE ALERT" in captured.out
    assert "ROLLBACK" in captured.out
    assert "Rollback occurred." in captured.out


def test_alert_factory_returns_alert_manager():
    from src.alerts.alert_factory import get_alert_manager
    from src.alerts.alert_manager import AlertManager

    alert_manager = get_alert_manager()

    assert isinstance(alert_manager, AlertManager)


def test_alert_factory_returns_console_manager():
    from src.alerts.alert_factory import get_alert_manager
    from src.alerts.console_alert import ConsoleAlertManager

    alert_manager = get_alert_manager()

    assert isinstance(alert_manager, ConsoleAlertManager)
