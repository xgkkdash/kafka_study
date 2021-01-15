import faust
from database import get_db
from database.mongodb import insert_order, find_order, update_order
from models.order import Order

app = faust.App(
    'order_svc',
    broker='kafka://localhost:9092',
)

order_in = app.topic('order_in', value_type=Order)
order_out = app.topic('order_out', value_type=Order)


db = get_db()


@app.agent(order_in)
async def on_order(orders):
    async for order in orders:
        print("received order: ", order)
        order_doc = await find_order(db, order.order_id)
        if order_doc:
            await update_order(db, order)
        else:
            await insert_order(db, order)
        yield order
        await order_out.send(value=order)
