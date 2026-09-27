import pandas as pd

from src.validation.schema import OrdersSchema


def test_valid_orders_data():
    data = pd.read_csv("data/raw/orders_v1.csv")

    validated_data = OrdersSchema.validate(data)

    assert len(validated_data) == 5