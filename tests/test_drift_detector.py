from src.detection.drift_detector import detect_schema_drift


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


def test_no_schema_drift():
    result = detect_schema_drift(
        EXPECTED_COLUMNS,
        EXPECTED_COLUMNS,
    )

    assert result["has_drift"] is False
    assert result["missing_columns"] == []
    assert result["unexpected_columns"] == []
    assert result["dtype_mismatches"] == {}


def test_schema_drift_detected():
    actual = [
        "client_id",
        "customer_name",
        "email",
        "age",
        "product",
        "quantity",
        "price",
        "order_date",
    ]

    result = detect_schema_drift(
        EXPECTED_COLUMNS,
        actual,
    )

    assert result["has_drift"] is True
    assert result["missing_columns"] == ["customer_id"]
    assert result["unexpected_columns"] == ["client_id"]


def test_datatype_drift_detected():
    expected_dtypes = {
        "customer_id": "object",
        "age": "int64",
        "price": "int64",
    }

    actual_dtypes = {
        "customer_id": "object",
        "age": "object",
        "price": "int64",
    }

    result = detect_schema_drift(
        ["customer_id", "age", "price"],
        ["customer_id", "age", "price"],
        expected_dtypes,
        actual_dtypes,
    )

    assert result["has_drift"] is True
    assert result["dtype_mismatches"]["age"]["expected"] == "int64"
    assert result["dtype_mismatches"]["age"]["actual"] == "object"
