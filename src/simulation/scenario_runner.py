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


SCENARIOS = {
    "healthy": "data/raw/orders_v1.csv",
    "renamed_column": "data/raw/orders_v2_renamed_column.csv",
    "datatype_drift": "data/raw/orders_v3_datatype_drift.csv",
}


def run_scenario(name: str) -> dict:
    """Run one predefined pipeline failure scenario."""

    if name not in SCENARIOS:
        raise ValueError(
            f"Unknown scenario: {name}"
        )

    data = pd.read_csv(SCENARIOS[name])

    result = run_pipeline(
        data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    return {
        "scenario": name,
        "status": result["status"],
        "risk": result["risk"],
        "decision": result["decision"],
        "validation": result["validation"],
    }


def run_all_scenarios() -> list[dict]:
    """Run all predefined scenarios."""

    return [
        run_scenario(name)
        for name in SCENARIOS
    ]
