import pandas as pd
import pytest

from src.simulation.failure_simulator import rename_column, change_datatype, remove_column


def test_rename_column():
    data = pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "customer_name": ["Arjun", "Priya"],
    })

    simulated_data = rename_column(
        data,
        "customer_id",
        "client_id",
    )

    assert "customer_id" not in simulated_data.columns
    assert "client_id" in simulated_data.columns
    assert "customer_name" in simulated_data.columns


def test_original_data_is_not_modified():
    data = pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "customer_name": ["Arjun", "Priya"],
    })

    rename_column(
        data,
        "customer_id",
        "client_id",
    )

    assert "customer_id" in data.columns
    assert "client_id" not in data.columns


def test_rename_missing_column_fails():
    data = pd.DataFrame({
        "customer_id": ["C001"]
    })

    with pytest.raises(ValueError):
        rename_column(
            data,
            "email",
            "client_email",
        )


def test_rename_to_existing_column_fails():
    data = pd.DataFrame({
        "customer_id": ["C001"],
        "client_id": ["C001"],
    })

    with pytest.raises(ValueError):
        rename_column(
            data,
            "customer_id",
            "client_id",
        )


def test_change_datatype():
    data = pd.DataFrame({
        "age": [21, 24, 22]
    })

    simulated_data = change_datatype(
        data,
        "age",
        "str",
    )

    assert simulated_data["age"].dtype == "str"
    assert simulated_data["age"].tolist() == ["21", "24", "22"]


def test_change_datatype_does_not_modify_original():
    data = pd.DataFrame({
        "age": [21, 24, 22]
    })

    change_datatype(
        data,
        "age",
        "str",
    )

    assert data["age"].dtype == "int64"


def test_change_datatype_missing_column_fails():
    data = pd.DataFrame({
        "age": [21, 24, 22]
    })

    with pytest.raises(ValueError):
        change_datatype(
            data,
            "salary",
            "str",
        )


def test_remove_column():
    data = pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "customer_name": ["Arjun", "Priya"],
        "age": [21, 24],
    })

    simulated_data = remove_column(
        data,
        "customer_id",
    )

    assert "customer_id" not in simulated_data.columns
    assert "customer_name" in simulated_data.columns
    assert "age" in simulated_data.columns


def test_remove_column_does_not_modify_original():
    data = pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "customer_name": ["Arjun", "Priya"],
    })

    remove_column(
        data,
        "customer_id",
    )

    assert "customer_id" in data.columns


def test_remove_missing_column_fails():
    data = pd.DataFrame({
        "customer_id": ["C001"]
    })

    with pytest.raises(ValueError):
        remove_column(
            data,
            "email",
        )
