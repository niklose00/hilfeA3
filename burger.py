from burgertypes import get_burger_type_random_choice
from numpy.random import default_rng

class Burger:
    def __init__(self, rng_burger_types):
        self.burger_machines = get_burger_type_random_choice(rng_burger_types)
