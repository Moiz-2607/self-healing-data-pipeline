import pandas as pd


def rename_column(
    data: pd.DataFrame,
    old_name: str,
    new_name: str,
) -> pd.DataFrame:
    """Create a copy of the data with one column renamed."""

    simulated_data = data.copy()

    if old_name not in simulated_data.columns:
        raise ValueError(
            f"Column '{old_name}' does not exist in the dataset."
        )

    if new_name in simulated_data.columns:
        raise ValueError(
            f"Column '{new_name}' already exists in the dataset."
        )

    simulated_data = simulated_data.rename(
        columns={old_name: new_name}
    )

    return simulated_data


def change_datatype(
    data: pd.DataFrame,
    column: str,
    target_dtype: str,
) -> pd.DataFrame:
    """Create a copy of the data with a simulated datatype change."""

    simulated_data = data.copy()

    if column not in simulated_data.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    if target_dtype == "str":
        simulated_data[column] = simulated_data[column].astype("str")

    elif target_dtype == "int64":
        simulated_data[column] = pd.to_numeric(
            simulated_data[column],
            errors="raise",
        ).astype("int64")

    else:
        raise ValueError(
            f"Unsupported target datatype: {target_dtype}"
        )

    return simulated_data


def remove_column(
    data: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """Create a copy of the data with one column removed."""

    simulated_data = data.copy()

    if column not in simulated_data.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    simulated_data = simulated_data.drop(columns=[column])

    return simulated_data
