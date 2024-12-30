import itertools

from burger import Burger

ORDER_ID_GENERATOR = itertools.count(1)     # ID generator for generating IDs for the orders

class Order:
    def __init__(self, env):
        self.burger = Burger()
        self.order_id = next(ORDER_ID_GENERATOR)
        self.order_time = env.now
        self.throughput_time = None
        self.pickup_time = env.now + 1800
        self.delay_time = 0
