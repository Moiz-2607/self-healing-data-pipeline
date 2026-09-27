from src.risk.classifier import classify_risk


def test_no_drift_is_low_risk():
    drift = {
        "has_drift": False,
        "missing_columns": [],
        "unexpected_columns": [],
        "dtype_mismatches": {},
    }

    result = classify_risk(drift)

    assert result["risk_level"] == "LOW"


def test_missing_column_is_high_risk():
    drift = {
        "has_drift": True,
        "missing_columns": ["customer_id"],
        "unexpected_columns": [],
        "dtype_mismatches": {},
    }

    result = classify_risk(drift)

    assert result["risk_level"] == "HIGH"


def test_unexpected_column_is_medium_risk():
    drift = {
        "has_drift": True,
        "missing_columns": [],
        "unexpected_columns": ["client_id"],
        "dtype_mismatches": {},
    }

    result = classify_risk(drift)

    assert result["risk_level"] == "MEDIUM"


def test_datatype_mismatch_is_low_risk():
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

    result = classify_risk(drift)

    assert result["risk_level"] == "LOW"
