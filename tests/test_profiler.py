import pandas as pd

from src.validation.profiler import profile_dataframe


def test_profile_dataframe():
    data = pd.read_csv("data/raw/orders_v1.csv")

    profile = profile_dataframe(data)

    assert profile["row_count"] == 5
    assert profile["column_count"] == 8
    assert "customer_id" in profile["columns"]
    assert profile["dtypes"]["price"] == "int64"
