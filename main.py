import os
import numpy as np
import simpy
from scipy.stats import norm
import itertools


from order import Order
from writer import save_waiting_processes_at_time_dic, set_output_folder, set_simulation_output_folder,\
    save_average_waiting_queue_time, save_average_throughput_times
from numpy.random import default_rng

SEED = 42

SIM_TIME = 10800
DELIMITER_FOR_SIMULATION_OUTPUT = ""
NUM_SIMULATIONS = 1
OUTPUT_FOLDER = "output"
STRATEGY = "FIFO"

MACHINE_CAPACITY_ONE = 1
MACHINE_CAPACITY_TWO = 1
MACHINE_CAPACITY_THREE = 1
MACHINE_CAPACITY_FOUR = 1
MACHINE_CAPACITY_FIVE = 1

ORDER_ID_GENERATOR = itertools.count(1)
rng_strategy_random = default_rng(SEED)
rng_timeBetweenOrders_random = default_rng(SEED)
rng_burger_types = default_rng(SEED)

def setup_waiting_queue_time():
    return {
            "M1": 0,
            "M2": 0,
            "M3": 0,
            "M4": 0,
            "M5": 0,
        }

def setup_last_queue_update():
    return {
            "M1": None,
            "M2": None,
            "M3": None,
            "M4": None,
            "M5": None,
        }

def setup_burger_throughput_times():
    return {
        "Type_1": [],
        "Type_2": [],
        "Type_3": [],
        "Type_4": [],
    }

def setup_occupancy_rate():
    return {
        "M1": 0,
        "M2": 0,
        "M3": 0,
        "M4": 0,
        "M5": 0,
    }

WAITING_QUEUE_TIME = setup_waiting_queue_time()

LAST_QUEUE_UPDATE = setup_last_queue_update()

BURGER_THROUGHPUT_TIMES = setup_burger_throughput_times()

OCCUPANCY_RATE = setup_occupancy_rate()


class BurgerStation:
    def __init__(self, env):
        self.env = env
        self.machine_one = simpy.PriorityResource(env, capacity=MACHINE_CAPACITY_ONE)
        self.machine_two = simpy.PriorityResource(env, capacity=MACHINE_CAPACITY_TWO)
        self.machine_three = simpy.PriorityResource(env, capacity=MACHINE_CAPACITY_THREE)
        self.machine_four = simpy.PriorityResource(env, capacity=MACHINE_CAPACITY_FOUR)
        self.machine_five = simpy.PriorityResource(env, capacity=MACHINE_CAPACITY_FIVE)

    def main_process(self, order_of_burger):
        machine_mapping = {
            "M1": (1, self.machine_one.queue, self.machine_one),
            "M2": (2, self.machine_two.queue, self.machine_two),
            "M3": (3, self.machine_three.queue, self.machine_three),
            "M4": (4, self.machine_four.queue, self.machine_four),
            "M5": (5, self.machine_five.queue, self.machine_five),
        }

        for machine in order_of_burger.burger.burger_machines:
            if isinstance(machine, str):
                continue
            machine_id, machine_queue, machine_resource = machine_mapping[machine[0]]
            yield self.env.process(self.process_machine(order_of_burger, machine, machine_id, machine_queue, machine_resource))

        order_of_burger.throughput_time = self.env.now - order_of_burger.order_time
        add_throughput_time(order_of_burger.burger.burger_machines[0], order_of_burger.throughput_time)


    def process_machine(self, order, machine_settings, machine_id, machine_queue, machine_resource):
        global WAITING_QUEUE_TIME, LAST_QUEUE_UPDATE

        timeout = get_waiting_time(order.rng, machine_settings)
        prio = get_priority_value_based_on_strategy(timeout, self.env.now, order.pickup_time)

        # print(order.order_id, f",{machine_id},", timeout)

        if len(machine_queue) > 0:
            if LAST_QUEUE_UPDATE[f"M{machine_id}"] is None:
                LAST_QUEUE_UPDATE[f"M{machine_id}"] = self.env.now

        with machine_resource.request(priority=prio) as request:
            yield request

            if len(machine_queue) == 0:
                if LAST_QUEUE_UPDATE[f"M{machine_id}"] is not None:
                    WAITING_QUEUE_TIME[f"M{machine_id}"] += self.env.now - LAST_QUEUE_UPDATE[f"M{machine_id}"]
                LAST_QUEUE_UPDATE[f"M{machine_id}"] = None

            OCCUPANCY_RATE[f"M{machine_id}"] += timeout
            yield self.env.timeout(timeout)



def get_waiting_time(rng, machine_setting):
    if machine_setting[1] == 'normal':
        return max(0,rng.normal(loc=machine_setting[2], scale=machine_setting[3]))
    elif machine_setting[1] == 'exponential':
        return rng.exponential(machine_setting[2])
    elif machine_setting[1] == 'uniform':
        return rng.uniform(machine_setting[2], machine_setting[3])
    else:
        raise ValueError(f"Unbekannte Verteilung: {machine_setting[1]}")

def print_stats(res):
    print(f'{res.count} of {res.capacity} slots are allocated.')
    print(f'  Users: {res.users}')
    print(f'  Queued events: {res.queue}')

    for item in res.users:
        print(item.__dict__)

def add_throughput_time(burger_type, throughput_time):
    if burger_type not in BURGER_THROUGHPUT_TIMES:
        BURGER_THROUGHPUT_TIMES[burger_type] = []
    BURGER_THROUGHPUT_TIMES[burger_type].append(throughput_time)

def setup(env):
    burger_station = BurgerStation(env)

    while env.now < SIM_TIME:
        time_between_orders = rng_timeBetweenOrders_random.exponential(scale=90)
        yield env.timeout(time_between_orders)

        order_of_burger = Order(env, rng_burger_types, ORDER_ID_GENERATOR)
        env.process(burger_station.main_process(order_of_burger))

def analyze_waiting_times():
    print("\n--- Wartezeit-Auswertung pro Maschine ---")
    for machine, waiting_time in WAITING_QUEUE_TIME.items():
        print(f"Maschine {machine}: Gesamtwartezeit = {waiting_time:.2f} Sekunden")

def analyze_occupancy_rate():
    print("\n--- Wartezeit-Auswertung pro Maschine ---")
    for machine, besetzungszeit in OCCUPANCY_RATE.items():
        print(besetzungszeit)
        print(f"Maschine {machine}: Gesamtwartezeit = {(besetzungszeit/SIM_TIME) * 100:.2f} %")

def analyze_throughput_times():
    print("\n--- Durchlaufzeit-Analyse pro Burgertyp ---")
    overall = 0
    for burger_type, times in BURGER_THROUGHPUT_TIMES.items():
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            overall += sum(times)
            print(f"Burgertyp: {burger_type} ({len(times)}-mal hergestellt)")
            print(f"  Durchschnittliche Durchlaufzeit: {avg_time:.2f} Sekunden")
            print(f"  Maximale Durchlaufzeit: {max_time:.2f} Sekunden")
            print(f"  Minimale Durchlaufzeit: {min_time:.2f} Sekunden")
        else:
            print(f"Burgertyp: {burger_type} hat keine Durchlaufzeiten.")

    print(f"  Insgesamte Durchlaufzeit: {overall:.2f} Sekunden")
    

def collecting_waiting_queue_time():
    TOTAL_WAITING_QUEUE_TIME["M1"] += WAITING_QUEUE_TIME["M1"]
    TOTAL_WAITING_QUEUE_TIME["M2"] += WAITING_QUEUE_TIME["M2"]
    TOTAL_WAITING_QUEUE_TIME["M3"] += WAITING_QUEUE_TIME["M3"]
    TOTAL_WAITING_QUEUE_TIME["M4"] += WAITING_QUEUE_TIME["M4"]
    TOTAL_WAITING_QUEUE_TIME["M5"] += WAITING_QUEUE_TIME["M5"]

def calculate_average_waiting_queue_time():
    for waiting_time_queue in TOTAL_WAITING_QUEUE_TIME:
        TOTAL_WAITING_QUEUE_TIME[waiting_time_queue] = TOTAL_WAITING_QUEUE_TIME[waiting_time_queue] / float(NUM_SIMULATIONS)

def collecting_throughput_times():
    for key, value in BURGER_THROUGHPUT_TIMES.items():
        TOTAL_BURGER_THROUGHPUT_TIMES[key].extend(value)

def get_priority_value_based_on_strategy(timeout, timestamp, earliest_due_date):
    strategies = {
        "FIFO": lambda: (timestamp * 10),
        "LIFO": lambda: (-timestamp * 10),
        "SPT": lambda: (timeout*1000),
        "LPT": lambda: (-timeout * 1000),
        "RANDOM": lambda: (rng_strategy_random.random() * 100),
        "EDD": lambda: earliest_due_date,
    }

    if STRATEGY not in strategies:
        raise ValueError(f"Unbekannte Priorisierungsstrategie: '{STRATEGY}'. Verfügbare Strategien: {list(strategies.keys())}")

    value = int(strategies[STRATEGY]())
    # print(value)
    return  value

    
if __name__ == '__main__':
    set_output_folder(OUTPUT_FOLDER)
    TOTAL_WAITING_QUEUE_TIME = setup_waiting_queue_time()
    TOTAL_BURGER_THROUGHPUT_TIMES = setup_burger_throughput_times()

    for simulation in range(0, NUM_SIMULATIONS):
        simulation_folder = set_simulation_output_folder(OUTPUT_FOLDER, simulation)

        env = simpy.Environment()
        env.process(setup(env))

        env.run()

        analyze_waiting_times()
        analyze_throughput_times()

        save_waiting_processes_at_time_dic(os.path.join(simulation_folder, "WAITING_QUEUE_TIME.csv"), WAITING_QUEUE_TIME, False)
        save_waiting_processes_at_time_dic(os.path.join(simulation_folder, "BURGER_THROUGHPUT_TIMES.csv"), BURGER_THROUGHPUT_TIMES, True)

        # Collect the information
        collecting_waiting_queue_time()
        collecting_throughput_times()

        # Reset data structures for the next iteration
        WAITING_QUEUE_TIME = setup_waiting_queue_time()
        LAST_QUEUE_UPDATE = setup_last_queue_update()
        BURGER_THROUGHPUT_TIMES = setup_burger_throughput_times()
        OCCUPANCY_RATE = setup_occupancy_rate()

        rng_strategy_random = default_rng(SEED)
        rng_timeBetweenOrders_random = default_rng(SEED)
        rng_burger_types = default_rng(SEED)
        ORDER_ID_GENERATOR = itertools.count(1)


    calculate_average_waiting_queue_time()
    save_average_waiting_queue_time(OUTPUT_FOLDER, "average_waiting_queue_time.csv", TOTAL_WAITING_QUEUE_TIME)
    save_average_throughput_times(OUTPUT_FOLDER, "throughput_times.csv", TOTAL_BURGER_THROUGHPUT_TIMES)