import asyncio
import motor


async def insert_order(db, order):
    order_dict = dict(order.__dict__)
    order_dict.pop("__evaluated_fields__", None)
    doc = await db.orders.insert_one(order_dict)
    return doc


async def find_order(db, order_id):
    doc = await db.orders.find_one({"order_id": order_id})
    return doc if doc else None


async def update_order(db, new_order):
    await db.orders.remove({"order_id": new_order.order_id})
    order_dict = dict(new_order.__dict__)
    order_dict.pop("__evaluated_fields__", None)
    doc = await db.orders.insert_one(order_dict)
    return doc


async def drop_orders(db):
    result = await db.orders.drop()
    return result

