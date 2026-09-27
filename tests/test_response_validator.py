import pytest

from src.ai.response_validator import validate_ai_diagnosis


def valid_diagnosis():
    return {
        "issue": "DATATYPE_DRIFT",
        "description": "Age has an incorrect datatype.",
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


def test_valid_ai_diagnosis():
    diagnosis = valid_diagnosis()

    result = validate_ai_diagnosis(diagnosis)

    assert result["suggested_action"] == "REPAIR_DATATYPE"
    assert result["confidence"] == 0.98
    assert len(result["repair_plan"]) == 1


def test_rejects_invalid_confidence():
    diagnosis = valid_diagnosis()
    diagnosis["confidence"] = 2.0

    with pytest.raises(ValueError):
        validate_ai_diagnosis(diagnosis)


def test_rejects_invalid_action():
    diagnosis = valid_diagnosis()
    diagnosis["suggested_action"] = "DROP_DATABASE"

    with pytest.raises(ValueError):
        validate_ai_diagnosis(diagnosis)


def test_rejects_invalid_operation():
    diagnosis = valid_diagnosis()
    diagnosis["repair_plan"][0]["operation"] = "DROP_COLUMN"

    with pytest.raises(ValueError):
        validate_ai_diagnosis(diagnosis)


def test_accepts_human_review():
    diagnosis = {
        "issue": "DATATYPE_DRIFT",
        "description": "The datatype is uncertain.",
        "suggested_action": "HUMAN_REVIEW",
        "confidence": 0.70,
        "repair_plan": [],
    }

    result = validate_ai_diagnosis(diagnosis)

    assert result["suggested_action"] == "HUMAN_REVIEW"
    assert result["repair_plan"] == []


def test_rejects_missing_required_field():
    diagnosis = valid_diagnosis()
    del diagnosis["confidence"]

    with pytest.raises(ValueError):
        validate_ai_diagnosis(diagnosis)


def test_rejects_non_list_repair_plan():
    diagnosis = valid_diagnosis()
    diagnosis["repair_plan"] = "CONVERT_DTYPE"

    with pytest.raises(ValueError):
        validate_ai_diagnosis(diagnosis)
