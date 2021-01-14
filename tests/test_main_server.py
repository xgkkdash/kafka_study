import pytest

from utils.util import gen_id
from main import app, Order, on_order


@pytest.fixture()
def app_for_test(event_loop):
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app


@pytest.mark.asyncio()
async def test_on_order(app_for_test):
    order = Order(gen_id(), "BTC/USD", "buy", 3000, 0.1)
    async with on_order.test_context() as agent:
        event = await agent.put(order)
        assert event.value.order_id == order.order_id

