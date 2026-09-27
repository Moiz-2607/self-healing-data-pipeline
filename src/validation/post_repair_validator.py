import pandas as pd

from src.detection.drift_detector import detect_schema_drift
from src.validation.profiler import profile_dataframe


def validate_repaired_data(
    data: pd.DataFrame,
    expected_columns: list[str],
    expected_dtypes: dict[str, str],
) -> dict:
    """Validate data after a repair attempt."""

    profile = profile_dataframe(data)

    drift = detect_schema_drift(
        expected_columns=expected_columns,
        actual_columns=profile["columns"],
        expected_dtypes=expected_dtypes,
        actual_dtypes=profile["dtypes"],
    )

    return {
        "valid": not drift["has_drift"],
        "drift": drift,
    }
