import pandas as pd

from src.validation.post_repair_validator import validate_repaired_data


EXPECTED_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "age",
    "product",
    "quantity",
    "price",
    "order_date",
]

EXPECTED_DTYPES = {
    "customer_id": "str",
    "customer_name": "str",
    "email": "str",
    "age": "int64",
    "product": "str",
    "quantity": "int64",
    "price": "int64",
    "order_date": "str",
}


def test_valid_repaired_data_passes():
    data = pd.DataFrame({
        "customer_id": ["C001"],
        "customer_name": ["Arjun Mehta"],
        "email": ["arjun@example.com"],
        "age": [21],
        "product": ["Laptop"],
        "quantity": [1],
        "price": [65000],
        "order_date": ["2026-09-20"],
    })

    result = validate_repaired_data(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["valid"] is True
    assert result["drift"]["has_drift"] is False


def test_invalid_repaired_data_fails():
    data = pd.DataFrame({
        "customer_id": ["C001"],
        "customer_name": ["Arjun Mehta"],
        "email": ["arjun@example.com"],
        "age": ["twenty-one"],
        "product": ["Laptop"],
        "quantity": [1],
        "price": [65000],
        "order_date": ["2026-09-20"],
    })

    result = validate_repaired_data(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["valid"] is False
    assert result["drift"]["has_drift"] is True
    assert "age" in result["drift"]["dtype_mismatches"]
