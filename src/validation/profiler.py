import pandas as pd


def profile_dataframe(data: pd.DataFrame) -> dict:
    """Generate a basic profile of a dataframe."""

    profile = {
        "columns": list(data.columns),
        "dtypes": {
            column: str(dtype)
            for column, dtype in data.dtypes.items()
        },
        "row_count": len(data),
        "column_count": len(data.columns),
    }

    return profile
