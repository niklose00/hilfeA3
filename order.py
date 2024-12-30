import itertools

from burger import Burger
from numpy.random import default_rng

# ORDER_ID_GENERATOR = itertools.count(1)     # ID generator for generating IDs for the orders

class Order:
    def __init__(self, env, rng_burger_types, ORDER_ID_GENERATOR):
        self.burger = Burger(rng_burger_types)
        self.order_id = next(ORDER_ID_GENERATOR)
        self.rng = default_rng(seed=self.order_id)
        self.order_time = env.now
        self.throughput_time = None
        self.pickup_time = env.now + 1800
        self.delay_time = 0