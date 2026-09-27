import pandas as pd

from src.detection.schema_analyzer import analyze_schema


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


def test_analyze_healthy_data():
    data = pd.read_csv("data/raw/orders_v1.csv")

    result = analyze_schema(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["profile"]["row_count"] == 5
    assert result["drift"]["has_drift"] is False


def test_detect_renamed_column():
    data = pd.read_csv("data/raw/orders_v2_renamed_column.csv")

    result = analyze_schema(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["drift"]["has_drift"] is True
    assert result["drift"]["missing_columns"] == ["customer_id"]
    assert result["drift"]["unexpected_columns"] == ["client_id"]


def test_detect_datatype_drift():
    data = pd.read_csv("data/raw/orders_v3_datatype_drift.csv")

    result = analyze_schema(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["drift"]["has_drift"] is True
    assert "age" in result["drift"]["dtype_mismatches"]
    assert result["drift"]["dtype_mismatches"]["age"]["expected"] == "int64"
    assert result["drift"]["dtype_mismatches"]["age"]["actual"] == "str"
