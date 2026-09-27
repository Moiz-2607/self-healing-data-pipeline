from typing import Any


def diagnose_drift(drift: dict[str, Any]) -> dict[str, Any]:
    """
    Produce a structured diagnosis from detected schema drift.

    The diagnosis recommends a possible recovery action,
    but it never modifies the data.
    """

    if not drift["has_drift"]:
        return {
            "issue": "NO_DRIFT",
            "description": "No schema drift detected.",
            "suggested_action": "NO_ACTION",
            "repair_plan": None,
            "confidence": 1.0,
        }

    if drift["dtype_mismatches"]:
        mismatches = []
        repair_plan = []

        for column, mismatch in drift["dtype_mismatches"].items():
            mismatches.append({
                "column": column,
                "expected_dtype": mismatch["expected"],
                "actual_dtype": mismatch["actual"],
                "suggested_action": f"Convert '{column}' to {mismatch['expected']}",
            })

            repair_plan.append({
                "operation": "CONVERT_DTYPE",
                "column": column,
                "from_dtype": mismatch["actual"],
                "to_dtype": mismatch["expected"],
            })

        return {
            "issue": "DATATYPE_DRIFT",
            "description": "One or more columns have datatype mismatches.",
            "mismatches": mismatches,
            "suggested_action": "REPAIR_DATATYPE",
            "repair_plan": repair_plan,
            "confidence": 0.98,
        }

    if drift["missing_columns"]:
        return {
            "issue": "MISSING_COLUMN",
            "description": "One or more required columns are missing.",
            "missing_columns": drift["missing_columns"],
            "suggested_action": "HUMAN_REVIEW",
            "repair_plan": None,
            "confidence": 0.99,
        }

    if drift["unexpected_columns"]:
        return {
            "issue": "UNEXPECTED_COLUMN",
            "description": "Unexpected columns were detected.",
            "unexpected_columns": drift["unexpected_columns"],
            "suggested_action": "HUMAN_REVIEW",
            "repair_plan": None,
            "confidence": 0.95,
        }

    return {
        "issue": "UNKNOWN_DRIFT",
        "description": "Schema drift was detected but could not be classified safely.",
        "suggested_action": "HUMAN_REVIEW",
        "repair_plan": None,
        "confidence": 0.50,
    }
