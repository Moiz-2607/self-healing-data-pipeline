import pandas as pd
import pytest

from src.repair.repair_engine import repair_datatype, execute_repair_plan


def test_repair_string_to_integer():
    data = pd.DataFrame({
        "age": ["21", "24", "22", "23", "25"]
    })

    repaired_data = repair_datatype(
        data,
        "age",
        "int64",
    )

    assert repaired_data["age"].dtype == "int64"
    assert repaired_data["age"].tolist() == [21, 24, 22, 23, 25]


def test_repair_invalid_integer_fails():
    data = pd.DataFrame({
        "age": ["21", "24", "twenty-two", "23", "25"]
    })

    with pytest.raises(ValueError):
        repair_datatype(
            data,
            "age",
            "int64",
        )


def test_repair_to_string():
    data = pd.DataFrame({
        "customer_id": [101, 102, 103]
    })

    repaired_data = repair_datatype(
        data,
        "customer_id",
        "str",
    )

    assert repaired_data["customer_id"].dtype == "str"


def test_execute_repair_plan():
    data = pd.DataFrame({
        "age": ["21", "24", "22"]
    })

    repair_plan = [
        {
            "operation": "CONVERT_DTYPE",
            "column": "age",
            "from_dtype": "str",
            "to_dtype": "int64",
        }
    ]

    repaired_data = execute_repair_plan(
        data,
        repair_plan,
    )

    assert repaired_data["age"].dtype == "int64"
    assert repaired_data["age"].tolist() == [21, 24, 22]


def test_execute_repair_plan_rejects_unknown_operation():
    data = pd.DataFrame({
        "age": [21, 24, 22]
    })

    repair_plan = [
        {
            "operation": "DELETE_DATA",
            "column": "age",
        }
    ]

    try:
        execute_repair_plan(
            data,
            repair_plan,
        )
        assert False
    except ValueError as error:
        assert "Unsupported repair operation" in str(error)
