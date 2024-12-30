from random import choice
import random

from numpy.random import Generator


def get_type_one():
    return [
        'Type_1',
        ('M4', 'normal', 40, 5),
        ('M2', 'normal', 10, 2),
        ('M1', 'exponential', 0.014),
        ('M3', 'uniform', 6, 14),
        ('M5', 'uniform', 5, 15)
    ]

def get_type_two():
    return [
        'Type_2',
        ('M1', 'exponential', 0.014),
        ('M4', 'normal', 35, 10),
        ('M5', 'exponential', 0.2),
        ('M2', 'uniform', 25, 45),
        ('M4', 'uniform', 30, 40),
        ('M3', 'exponential', 0.1)
    ]

def get_type_three():
    return [
        'Type_3',
        ('M4', 'normal', 100, 15),
        ('M2', 'uniform', 10, 20),
        ('M5', 'normal', 20, 5),
        ('M1', 'normal', 35, 10)
    ]

def get_type_four():
    return [
        'Type_4',
        ('M2', 'uniform', 20, 30),
        ('M1', 'exponential', 0.043),
        ('M5', 'normal', 40, 4),
        ('M3', 'normal', 25, 5),
        ('M4', 'uniform', 50, 60)
    ]



methods = [get_type_one(), get_type_two(), get_type_three(), get_type_four()]


def get_burger_type_random_choice(rng: Generator):
    choice = rng.choice([0,1,2,3])
    return methods[choice]
    


# if __name__ == '__main__':
#     BURGER_TYPE_SEED = 12345
#     rng_burger_types = default_rng(BURGER_TYPE_SEED)
#     for i in range(10):  # 10 Iterationen
#         get_burger_type_random_choice(rng_burger_types)