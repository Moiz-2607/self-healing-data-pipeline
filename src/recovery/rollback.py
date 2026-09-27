import pandas as pd


def create_backup(data: pd.DataFrame) -> pd.DataFrame:
    """Create a backup copy before a repair attempt."""

    return data.copy(deep=True)


def rollback(
    original_data: pd.DataFrame,
) -> pd.DataFrame:
    """Restore the original data after a failed repair."""

    return original_data.copy(deep=True)
