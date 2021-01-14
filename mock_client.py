import faust
from models.order import Order
from utils.util import gen_id

app = faust.App(
    'mock_client',
    web_port=7001
)

order_in = app.topic('order_in', value_type=Order)


@app.timer(2.0, on_leader=True)
async def publish_order():
    order = Order(gen_id(), "BTC/USD", "buy", 3000, 0.1)
    print("generated: ", order)
    await order_in.send(value=order)
