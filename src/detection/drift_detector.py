from typing import Any


def detect_schema_drift(
    expected_columns: list[str],
    actual_columns: list[str],
    expected_dtypes: dict[str, str] | None = None,
    actual_dtypes: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Compare expected and actual schema information."""

    expected = set(expected_columns)
    actual = set(actual_columns)

    missing_columns = sorted(expected - actual)
    unexpected_columns = sorted(actual - expected)

    dtype_mismatches = {}

    if expected_dtypes and actual_dtypes:
        for column in expected & actual:
            if expected_dtypes.get(column) != actual_dtypes.get(column):
                dtype_mismatches[column] = {
                    "expected": expected_dtypes.get(column),
                    "actual": actual_dtypes.get(column),
                }

    has_drift = bool(
        missing_columns
        or unexpected_columns
        or dtype_mismatches
    )

    return {
        "has_drift": has_drift,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "dtype_mismatches": dtype_mismatches,
    }
