from src.decision.decision_engine import make_recovery_decision


def test_low_risk_high_confidence_allows_auto_repair():
    risk = {
        "risk_level": "LOW"
    }

    diagnosis = {
        "confidence": 0.98
    }

    result = make_recovery_decision(risk, diagnosis)

    assert result["action"] == "AUTO_REPAIR"


def test_low_risk_low_confidence_requires_ai_suggestion():
    risk = {
        "risk_level": "LOW"
    }

    diagnosis = {
        "confidence": 0.70
    }

    result = make_recovery_decision(risk, diagnosis)

    assert result["action"] == "AI_SUGGESTION"


def test_medium_risk_requires_ai_suggestion():
    risk = {
        "risk_level": "MEDIUM"
    }

    diagnosis = {
        "confidence": 0.99
    }

    result = make_recovery_decision(risk, diagnosis)

    assert result["action"] == "AI_SUGGESTION"


def test_high_risk_always_requires_human_review():
    risk = {
        "risk_level": "HIGH"
    }

    diagnosis = {
        "confidence": 0.99
    }

    result = make_recovery_decision(risk, diagnosis)

    assert result["action"] == "HUMAN_REVIEW"


def test_unknown_risk_requires_human_review():
    risk = {
        "risk_level": "UNKNOWN"
    }

    diagnosis = {
        "confidence": 0.99
    }

    result = make_recovery_decision(risk, diagnosis)

    assert result["action"] == "HUMAN_REVIEW"


def test_deterministic_fallback_allows_safe_datatype_repair():
    risk = {
        "risk_level": "LOW",
        "reason": "Datatype mismatch detected.",
    }

    ai_diagnosis = {
        "issue": "Datatype mismatch",
        "description": "The AI is uncertain about the repair.",
        "suggested_action": "HUMAN_REVIEW",
        "confidence": 0.70,
        "repair_plan": [],
    }

    fallback_diagnosis = {
        "issue": "DATATYPE_DRIFT",
        "description": "Known datatype mismatch.",
        "suggested_action": "REPAIR_DATATYPE",
        "confidence": 0.98,
        "repair_plan": [
            {
                "operation": "CONVERT_DTYPE",
                "column": "age",
                "from_dtype": "str",
                "to_dtype": "int64",
            }
        ],
    }

    result = make_recovery_decision(
        risk,
        ai_diagnosis,
        fallback_diagnosis=fallback_diagnosis,
    )

    assert result["action"] == "AUTO_REPAIR"
