import faust
from models.order import Order

app = faust.App(
    'mock_server',
    web_port=7002
)

order_out = app.topic('order_out', value_type=Order)


@app.agent(order_out)
async def process(stream):
    async for o in stream:
        print("processing order: ", o)
        yield o
