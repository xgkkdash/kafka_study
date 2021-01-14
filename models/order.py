import faust


class Order(faust.Record):
    order_id: str
    symbol: str
    side: str
    price: float
    quantity: float

    def __abstract_init__(self) -> None:
        pass
