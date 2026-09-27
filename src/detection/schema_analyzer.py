import pandas as pd

from src.validation.profiler import profile_dataframe
from src.detection.drift_detector import detect_schema_drift


def analyze_schema(
    data: pd.DataFrame,
    expected_columns: list[str],
    expected_dtypes: dict[str, str],
) -> dict:
    """Profile incoming data and detect schema drift."""

    profile = profile_dataframe(data)

    drift = detect_schema_drift(
        expected_columns=expected_columns,
        actual_columns=profile["columns"],
        expected_dtypes=expected_dtypes,
        actual_dtypes=profile["dtypes"],
    )

    return {
        "profile": profile,
        "drift": drift,
    }
