import faust
import mode
from mode import Service
from models.order import Order


class OrderService(Service):
    pubsub = faust.App('pubsub_order')
    order_in = pubsub.topic('order_in', value_type=Order)
    order_out = pubsub.topic('order_out', value_type=Order)

    def __post_init__(self) -> None:
        """Additional user initialization."""
        self.add_dependency(self.pubsub)

    async def on_first_start(self) -> None:
        """Service started for the first time in this process."""
        self.log.info(self.label + ' first starting')

    async def on_start(self) -> None:
        """Service is starting."""
        self.log.info(self.label + ' starting')

    async def on_started(self) -> None:
        """Service has started."""
        self.log.info(self.label + ' started')

    async def on_stop(self) -> None:
        """Service is being stopped/restarted."""
        self.log.info(self.label + ' stopping')

    async def on_shutdown(self) -> None:
        """Service is stopped and shutdown."""
        self.log.info(self.label + ' shutdown')

    async def on_restart(self) -> None:
        """Service is being restarted."""
        self.log.info(self.label + ' restarting')

    @pubsub.agent(order_in)
    async def on_order(orders):
        async for order in orders:
            print("mode_svc received order: ", order)
            yield order


if __name__ == '__main__':
    worker = mode.Worker(OrderService(), loglevel='info')
    worker.execute_from_commandline()
