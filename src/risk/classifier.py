from typing import Any


def classify_risk(drift: dict[str, Any]) -> dict[str, str]:
    """Classify schema drift according to its potential repair risk."""

    if not drift["has_drift"]:
        return {
            "risk_level": "LOW",
            "reason": "No schema drift detected.",
        }

    if drift["missing_columns"]:
        return {
            "risk_level": "HIGH",
            "reason": "Required columns are missing.",
        }

    if drift["unexpected_columns"]:
        return {
            "risk_level": "MEDIUM",
            "reason": "Unexpected columns were detected.",
        }

    if drift["dtype_mismatches"]:
        return {
            "risk_level": "LOW",
            "reason": "Datatype mismatch detected.",
        }

    return {
        "risk_level": "HIGH",
        "reason": "Unknown schema drift detected.",
    }
