import pandas as pd

from src.pipeline import run_pipeline
from src.simulation.failure_simulator import (
    rename_column,
    change_datatype,
    remove_column,
)


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


def run_scenario(name, simulated_data):
    print(f"\n{'=' * 60}")
    print(name)
    print("=" * 60)

    result = run_pipeline(
        simulated_data,
        EXPECTED_COLUMNS,
        EXPECTED_DTYPES,
    )

    print("Status:", result["status"])
    print("Risk:", result["risk"]["risk_level"])

    diagnosis = result["diagnosis"]

    print("\nDiagnosis:")
    print("  Issue:", diagnosis["issue"])
    print("  Description:", diagnosis["description"])
    print("  Confidence:", diagnosis["confidence"])

    decision = result["decision"]

    print("\nDecision:")
    print("  Action:", decision["action"])
    print("  Reason:", decision["reason"])

    repair_plan = diagnosis.get("repair_plan")

    if repair_plan:
        print("\nRepair Plan:")

        for operation in repair_plan:
            print("  Operation:", operation["operation"])
            print("  Column:", operation["column"])
            print("  From:", operation["from_dtype"])
            print("  To:", operation["to_dtype"])

    print("\nMessage:", result["message"])

    return result


def main():
    data = pd.read_csv("data/raw/orders_v1.csv")

    print("\n=== SELF-HEALING DATA PIPELINE AGENT ===")

    run_scenario(
        "SCENARIO 1: RENAMED COLUMN",
        rename_column(
            data,
            "customer_id",
            "client_id",
        ),
    )

    run_scenario(
        "SCENARIO 2: DATATYPE DRIFT",
        change_datatype(
            data,
            "age",
            "str",
        ),
    )

    run_scenario(
        "SCENARIO 3: MISSING COLUMN",
        remove_column(
            data,
            "customer_id",
        ),
    )


if __name__ == "__main__":
    main()
