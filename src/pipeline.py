import pandas as pd

from src.detection.schema_analyzer import analyze_schema
from src.ai.provider import AIProvider
from src.ai.mock_provider import MockAIProvider
from src.diagnosis.diagnosis_engine import diagnose_drift
from src.risk.classifier import classify_risk
from src.decision.decision_engine import make_recovery_decision
from src.repair.repair_engine import execute_repair_plan
from src.validation.post_repair_validator import validate_repaired_data
from src.monitoring.audit_logger import log_event
from src.recovery.rollback import create_backup, rollback
from src.alerts.console_alert import ConsoleAlertManager


def run_pipeline(
    data: pd.DataFrame,
    expected_columns: list[str],
    expected_dtypes: dict[str, str],
    ai_provider: AIProvider | None = None,
    alert_manager: ConsoleAlertManager | None = None,
) -> dict:
    """
    Run detection, AI diagnosis, risk classification, decision,
    repair, validation, rollback, auditing, and alerting.
    """

    if ai_provider is None:
        ai_provider = MockAIProvider()

    if alert_manager is None:
        alert_manager = ConsoleAlertManager()

    analysis = analyze_schema(
        data,
        expected_columns,
        expected_dtypes,
    )

    drift = analysis["drift"]

    # Healthy data does not require AI diagnosis.
    if not drift["has_drift"]:
        log_event(
            "PIPELINE_SUCCESS",
            {
                "message": "No schema drift detected.",
                "status": "SUCCESS",
                "diagnosis": {
                    "issue": "NO_DRIFT",
                    "description": "No schema drift detected.",
                    "suggested_action": "NO_ACTION",
                    "repair_plan": None,
                    "confidence": 1.0,
                },
            },
        )

        return {
            "status": "SUCCESS",
            "message": "No schema drift detected.",
            "data": data,
            "risk": {
                "risk_level": "LOW",
                "reason": "No schema drift detected.",
            },
            "diagnosis": {
                "issue": "NO_DRIFT",
                "description": "No schema drift detected.",
                "suggested_action": "NO_ACTION",
                "repair_plan": None,
                "confidence": 1.0,
            },
            "decision": {
                "action": "NO_ACTION",
                "reason": "No recovery is required.",
            },
            "validation": {
                "valid": True,
            },
        }

    # Build a deterministic diagnosis for known-safe failure types.
    fallback_diagnosis = diagnose_drift(drift)

    # AI is only called when actual drift exists.
    diagnosis = ai_provider.diagnose(drift)

    risk = classify_risk(drift)

    decision = make_recovery_decision(
        risk,
        diagnosis,
        fallback_diagnosis=fallback_diagnosis,
    )

    if decision["action"] != "AUTO_REPAIR":
        log_event(
            "REVIEW_REQUIRED",
            {
                "risk_level": risk["risk_level"],
                "reason": risk["reason"],
                "diagnosis": diagnosis,
                "decision": decision,
                "missing_columns": drift["missing_columns"],
                "unexpected_columns": drift["unexpected_columns"],
            },
        )

        alert_manager.send_alert(
            "HUMAN_REVIEW",
            "High-risk or uncertain pipeline failure requires human review.",
            {
                "risk_level": risk["risk_level"],
                "status": "REVIEW_REQUIRED",
                "reason": decision["reason"],
            },
        )

        return {
            "status": "REVIEW_REQUIRED",
            "message": decision["reason"],
            "data": data,
            "risk": risk,
            "diagnosis": diagnosis,
            "decision": decision,
            "validation": {
                "valid": False,
            },
        }

    # Select the repair plan from the trusted deterministic
    # diagnosis when it authorized the automatic repair.
    repair_plan = diagnosis["repair_plan"]

    if (
        decision["action"] == "AUTO_REPAIR"
        and fallback_diagnosis.get("suggested_action") == "REPAIR_DATATYPE"
        and fallback_diagnosis.get("repair_plan")
    ):
        repair_plan = fallback_diagnosis["repair_plan"]

    backup = create_backup(data)
    repaired_data = data.copy()

    try:
        repaired_data = execute_repair_plan(
            repaired_data,
            repair_plan,
        )

    except (ValueError, TypeError) as error:
        restored_data = rollback(backup)

        log_event(
            "ROLLBACK",
            {
                "risk_level": risk["risk_level"],
                "final_status": "ROLLED_BACK",
                "reason": "Repair attempt failed.",
                "error": str(error),
                "ai_diagnosis": diagnosis,
                "deterministic_diagnosis": fallback_diagnosis,
                "decision": decision,
                "repair_plan_attempted": repair_plan,
                "validation": {
                    "valid": False,
                },
                "rollback": True,
            },
        )

        alert_manager.send_alert(
            "ROLLBACK",
            "Automatic repair failed. Original data was restored.",
            {
                "risk_level": risk["risk_level"],
                "status": "ROLLED_BACK",
                "error": str(error),
            },
        )

        return {
            "status": "ROLLED_BACK",
            "message": "Repair failed and original data was restored.",
            "data": restored_data,
            "risk": risk,
            "diagnosis": diagnosis,
            "decision": decision,
            "validation": {
                "valid": False,
            },
        }

    validation = validate_repaired_data(
        repaired_data,
        expected_columns,
        expected_dtypes,
    )

    if validation["valid"]:
        log_event(
            "REPAIR_SUCCESS",
            {
                "risk_level": risk["risk_level"],
                "final_status": "REPAIRED",
                "ai_diagnosis": diagnosis,
                "deterministic_diagnosis": fallback_diagnosis,
                "decision": decision,
                "repair_plan_used": repair_plan,
                "validation": validation,
                "rollback": False,
            },
        )

        return {
            "status": "REPAIRED",
            "message": "Data was repaired and validation passed.",
            "data": repaired_data,
            "risk": risk,
            "diagnosis": diagnosis,
            "decision": decision,
            "validation": validation,
        }

    restored_data = rollback(backup)

    log_event(
        "ROLLBACK",
        {
            "risk_level": risk["risk_level"],
            "final_status": "ROLLED_BACK",
            "reason": "Post-repair validation failed.",
            "ai_diagnosis": diagnosis,
            "deterministic_diagnosis": fallback_diagnosis,
            "decision": decision,
            "repair_plan_attempted": repair_plan,
            "validation": validation,
            "rollback": True,
        },
    )

    alert_manager.send_alert(
        "ROLLBACK",
        "Post-repair validation failed. Original data was restored.",
        {
            "risk_level": risk["risk_level"],
            "status": "ROLLED_BACK",
            "reason": "Post-repair validation failed.",
        },
    )

    return {
        "status": "ROLLED_BACK",
        "message": "Validation failed and original data was restored.",
        "data": restored_data,
        "risk": risk,
        "diagnosis": diagnosis,
        "decision": decision,
        "validation": validation,
    }
