import faust
from models.order import Order

app = faust.App(
    'order_svc',
    broker='kafka://localhost:9092',
)

order_in = app.topic('order_in', value_type=Order)
order_out = app.topic('order_out', value_type=Order)


@app.agent(order_in)
async def on_order(orders):
    async for order in orders:
        print("received order: ", order)
        yield order
        await order_out.send(value=order)
