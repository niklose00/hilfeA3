from burgertypes import get_burger_type_random_choice


class Burger:
    def __init__(self):
        self.burger_machines = get_burger_type_random_choice()