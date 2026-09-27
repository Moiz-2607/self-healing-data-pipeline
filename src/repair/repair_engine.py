import pandas as pd


def repair_datatype(
    data: pd.DataFrame,
    column: str,
    target_dtype: str,
) -> pd.DataFrame:
    """Attempt to convert a column to the expected datatype."""

    repaired_data = data.copy()

    if target_dtype == "int64":
        repaired_data[column] = pd.to_numeric(
            repaired_data[column],
            errors="raise",
        ).astype("int64")

    elif target_dtype == "str":
        repaired_data[column] = repaired_data[column].astype("str")

    else:
        raise ValueError(
            f"Unsupported target datatype: {target_dtype}"
        )

    return repaired_data


def execute_repair_plan(
    data: pd.DataFrame,
    repair_plan: list[dict],
) -> pd.DataFrame:
    """
    Execute a structured repair plan.

    Only explicitly supported repair operations are executed.
    """

    repaired_data = data.copy()

    for operation in repair_plan:
        operation_type = operation["operation"]

        if operation_type == "CONVERT_DTYPE":
            repaired_data = repair_datatype(
                repaired_data,
                operation["column"],
                operation["to_dtype"],
            )

        else:
            raise ValueError(
                f"Unsupported repair operation: {operation_type}"
            )

    return repaired_data
