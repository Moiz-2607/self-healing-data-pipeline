from src.ai.mock_provider import MockAIProvider


def test_mock_ai_provider_diagnoses_datatype_drift():
    drift = {
        "has_drift": True,
        "missing_columns": [],
        "unexpected_columns": [],
        "dtype_mismatches": {
            "age": {
                "expected": "int64",
                "actual": "str",
            }
        },
    }

    provider = MockAIProvider()

    result = provider.diagnose(drift)

    assert result["issue"] == "DATATYPE_DRIFT"
    assert result["confidence"] == 0.98
    assert result["suggested_action"] == "REPAIR_DATATYPE"
    assert result["repair_plan"][0]["operation"] == "CONVERT_DTYPE"


def test_mock_ai_provider_handles_missing_column():
    drift = {
        "has_drift": True,
        "missing_columns": ["customer_id"],
        "unexpected_columns": [],
        "dtype_mismatches": {},
    }

    provider = MockAIProvider()

    result = provider.diagnose(drift)

    assert result["issue"] == "MISSING_COLUMN"
    assert result["suggested_action"] == "HUMAN_REVIEW"
