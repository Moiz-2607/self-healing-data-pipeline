import pandera.pandas as pa
from pandera.typing import Series


class OrdersSchema(pa.DataFrameModel):
    customer_id: Series[str]
    customer_name: Series[str]
    email: Series[str]
    age: Series[int]
    product: Series[str]
    quantity: Series[int]
    price: Series[int]
    order_date: Series[str]

    class Config:
        strict = True