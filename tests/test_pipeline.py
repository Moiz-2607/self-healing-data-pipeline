import pandas as pd

from src.pipeline import run_pipeline


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


def test_healthy_data_pipeline():
    data = pd.read_csv("data/raw/orders_v1.csv")

    result = run_pipeline(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["status"] == "SUCCESS"
    assert result["validation"]["valid"] is True


def test_datatype_drift_is_repaired():
    data = pd.DataFrame({
        "customer_id": ["C001"],
        "customer_name": ["Arjun Mehta"],
        "email": ["arjun@example.com"],
        "age": ["21"],
        "product": ["Laptop"],
        "quantity": [1],
        "price": [65000],
        "order_date": ["2026-09-20"],
    })

    result = run_pipeline(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["status"] == "REPAIRED"
    assert result["validation"]["valid"] is True
    assert result["data"]["age"].dtype == "int64"


def test_missing_column_requires_review():
    data = pd.read_csv("data/raw/orders_v2_renamed_column.csv")

    result = run_pipeline(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["status"] == "REVIEW_REQUIRED"
    assert result["risk"]["risk_level"] == "HIGH"


def test_pipeline_rolls_back_when_repair_fails():
    data = pd.DataFrame({
        "customer_id": ["C001"],
        "customer_name": ["Arjun"],
        "email": ["arjun@example.com"],
        "age": ["twenty-two"],
        "product": ["Laptop"],
        "quantity": [1],
        "price": [65000],
        "order_date": ["2026-09-20"],
    })

    result = run_pipeline(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["status"] == "ROLLED_BACK"
    assert result["data"]["age"].iloc[0] == "twenty-two"
    assert result["validation"]["valid"] is False


class CustomAIProvider:
    def diagnose(self, drift):
        return {
            "issue": "DATATYPE_DRIFT",
            "description": "Custom provider diagnosis.",
            "suggested_action": "REPAIR_DATATYPE",
            "repair_plan": [
                {
                    "operation": "CONVERT_DTYPE",
                    "column": "age",
                    "from_dtype": "str",
                    "to_dtype": "int64",
                }
            ],
            "confidence": 0.99,
        }


def test_pipeline_accepts_custom_ai_provider():
    data = pd.DataFrame({
        "customer_id": ["C001"],
        "customer_name": ["Arjun"],
        "email": ["arjun@example.com"],
        "age": ["22"],
        "product": ["Laptop"],
        "quantity": [1],
        "price": [65000],
        "order_date": ["2026-09-20"],
    })

    provider = CustomAIProvider()

    result = run_pipeline(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
        ai_provider=provider,
    )

    assert result["status"] == "REPAIRED"
    assert result["diagnosis"]["confidence"] == 0.99
    assert result["data"]["age"].dtype == "int64"
