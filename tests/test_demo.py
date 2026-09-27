import pandas as pd

from src.pipeline import run_pipeline
from src.simulation.failure_simulator import rename_column


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


def test_simulated_rename_reaches_review():
    data = pd.read_csv("data/raw/orders_v1.csv")

    simulated_data = rename_column(
        data,
        "customer_id",
        "client_id",
    )

    result = run_pipeline(
        simulated_data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    assert result["status"] == "REVIEW_REQUIRED"
    assert result["risk"]["risk_level"] == "HIGH"
