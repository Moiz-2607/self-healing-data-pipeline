from src.diagnosis.diagnosis_engine import diagnose_drift


def test_no_drift_diagnosis():
    drift = {
        "has_drift": False,
        "missing_columns": [],
        "unexpected_columns": [],
        "dtype_mismatches": {},
    }

    result = diagnose_drift(drift)

    assert result["issue"] == "NO_DRIFT"
    assert result["suggested_action"] == "NO_ACTION"
    assert result["repair_plan"] is None
    assert result["confidence"] == 1.0


def test_datatype_drift_diagnosis():
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

    result = diagnose_drift(drift)

    assert result["issue"] == "DATATYPE_DRIFT"
    assert result["suggested_action"] == "REPAIR_DATATYPE"
    assert result["confidence"] == 0.98

    assert result["repair_plan"][0]["operation"] == "CONVERT_DTYPE"
    assert result["repair_plan"][0]["column"] == "age"
    assert result["repair_plan"][0]["from_dtype"] == "str"
    assert result["repair_plan"][0]["to_dtype"] == "int64"


def test_missing_column_requires_human_review():
    drift = {
        "has_drift": True,
        "missing_columns": ["customer_id"],
        "unexpected_columns": [],
        "dtype_mismatches": {},
    }

    result = diagnose_drift(drift)

    assert result["issue"] == "MISSING_COLUMN"
    assert result["suggested_action"] == "HUMAN_REVIEW"
    assert result["repair_plan"] is None


def test_unexpected_column_requires_human_review():
    drift = {
        "has_drift": True,
        "missing_columns": [],
        "unexpected_columns": ["client_id"],
        "dtype_mismatches": {},
    }

    result = diagnose_drift(drift)

    assert result["issue"] == "UNEXPECTED_COLUMN"
    assert result["suggested_action"] == "HUMAN_REVIEW"
    assert result["repair_plan"] is None


def test_datatype_drift_produces_safe_repair_plan():
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

    result = diagnose_drift(drift)

    assert result["issue"] == "DATATYPE_DRIFT"
    assert result["suggested_action"] == "REPAIR_DATATYPE"
    assert result["confidence"] >= 0.90
    assert result["repair_plan"] == [
        {
            "operation": "CONVERT_DTYPE",
            "column": "age",
            "from_dtype": "str",
            "to_dtype": "int64",
        }
    ]
