from typing import Any


def make_recovery_decision(
    risk: dict[str, Any],
    diagnosis: dict[str, Any],
    fallback_diagnosis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Decide how the system should respond to a diagnosed failure.

    The AI diagnosis is considered first, but a deterministic
    fallback diagnosis can authorize a known-safe repair.
    """

    risk_level = risk["risk_level"]
    confidence = diagnosis["confidence"]

    if risk_level == "HIGH":
        return {
            "action": "HUMAN_REVIEW",
            "reason": "High-risk failure requires human approval.",
        }

    if (
        fallback_diagnosis is not None
        and fallback_diagnosis.get("suggested_action") == "REPAIR_DATATYPE"
        and fallback_diagnosis.get("confidence", 0.0) >= 0.90
        and fallback_diagnosis.get("repair_plan")
    ):
        return {
            "action": "AUTO_REPAIR",
            "reason": (
                "A deterministic high-confidence repair plan "
                "is available for this known-safe failure."
            ),
        }

    if risk_level == "MEDIUM":
        return {
            "action": "AI_SUGGESTION",
            "reason": "Medium-risk failure requires additional reasoning and validation.",
        }

    if risk_level == "LOW" and confidence >= 0.90:
        return {
            "action": "AUTO_REPAIR",
            "reason": "Low-risk failure has high diagnostic confidence.",
        }

    if risk_level == "LOW":
        return {
            "action": "AI_SUGGESTION",
            "reason": "Diagnostic confidence is not high enough for automatic repair.",
        }

    return {
        "action": "HUMAN_REVIEW",
        "reason": "Recovery strategy could not be determined safely.",
    }
