import random
import os
import simpy
from scipy.stats import norm

from order import Order
from writer import save_waiting_processes_at_time_dic, set_output_folder, set_simulation_output_folder,\
    save_average_waiting_queue_time, save_average_throughput_times

SIM_TIME = 10800
DELIMITER_FOR_SIMULATION_OUTPUT = ""
NUM_SIMULATIONS = 1
OUTPUT_FOLDER = "output"
STRATEGY = "EDD"

MACHINE_CAPACITY_ONE = 1
MACHINE_CAPACITY_TWO = 1
MACHINE_CAPACITY_THREE = 1
MACHINE_CAPACITY_FOUR = 1
MACHINE_CAPACITY_FIVE = 1

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
        "Type_5": [],
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
        for machine in order_of_burger.burger.burger_machines:
            if machine[0] == "M1":
                yield self.env.process(self.machine_one_process(machine, order_of_burger.pickup_time))
            elif machine[0] == "M2":
                yield self.env.process(self.machine_two_process(machine, order_of_burger.pickup_time))
            elif machine[0] == "M3":
                yield self.env.process(self.machine_three_process(machine, order_of_burger.pickup_time))
            elif machine[0] == "M4":
                yield self.env.process(self.machine_four_process(machine, order_of_burger.pickup_time))
            elif machine[0] == "M5":
                yield self.env.process(self.machine_five_process(machine, order_of_burger.pickup_time))
                
        order_of_burger.throughput_time = self.env.now - order_of_burger.order_time
        add_throughput_time(order_of_burger.burger.burger_machines[0], order_of_burger.throughput_time)
         

    def machine_one_process(self, machine_settings, order_of_burger_pickup_time):
        global WAITING_QUEUE_TIME, LAST_QUEUE_UPDATE
        timeout = get_waiting_time(machine_settings)
        prio = get_priority_value_based_on_strategy(timeout, self.env.now, order_of_burger_pickup_time)

        if len(self.machine_one.queue) > 0:
            if LAST_QUEUE_UPDATE["M1"] is None:
                LAST_QUEUE_UPDATE["M1"] = self.env.now


        with self.machine_one.request(priority=prio) as request:
            yield request  

            if len(self.machine_one.queue) == 0:
                if LAST_QUEUE_UPDATE["M1"] is not None:  
                    WAITING_QUEUE_TIME["M1"] += self.env.now - LAST_QUEUE_UPDATE["M1"]
                LAST_QUEUE_UPDATE["M1"] = None

            OCCUPANCY_RATE["M1"] += timeout
            yield self.env.timeout(timeout)


    def machine_two_process(self, machine_settings, order_of_burger_pickup_time):
        global WAITING_QUEUE_TIME, LAST_QUEUE_UPDATE
        timeout = get_waiting_time(machine_settings)
        prio = get_priority_value_based_on_strategy(timeout, self.env.now, order_of_burger_pickup_time)

        if len(self.machine_two.queue) > 0:
            if LAST_QUEUE_UPDATE["M2"] is None:
                LAST_QUEUE_UPDATE["M2"] = self.env.now


        with self.machine_two.request(priority=prio) as request:
            yield request  

            if len(self.machine_two.queue) == 0:
                if LAST_QUEUE_UPDATE["M2"] is not None:  
                    WAITING_QUEUE_TIME["M2"] += self.env.now - LAST_QUEUE_UPDATE["M2"]
                LAST_QUEUE_UPDATE["M2"] = None

            OCCUPANCY_RATE["M2"] += timeout
            yield self.env.timeout(timeout)


    def machine_three_process(self, machine_settings, order_of_burger_pickup_time):
        global WAITING_QUEUE_TIME, LAST_QUEUE_UPDATE
        timeout = get_waiting_time(machine_settings)
        prio = get_priority_value_based_on_strategy(timeout, self.env.now, order_of_burger_pickup_time)

        if len(self.machine_three.queue) > 0:
            if LAST_QUEUE_UPDATE["M3"] is None:
                LAST_QUEUE_UPDATE["M3"] = self.env.now


        with self.machine_three.request(priority=prio) as request:
            yield request  

            if len(self.machine_three.queue) == 0:
                if LAST_QUEUE_UPDATE["M3"] is not None:  
                    WAITING_QUEUE_TIME["M3"] += self.env.now - LAST_QUEUE_UPDATE["M3"]
                LAST_QUEUE_UPDATE["M3"] = None

            OCCUPANCY_RATE["M3"] += timeout
            yield self.env.timeout(timeout)


    def machine_four_process(self, machine_settings, order_of_burger_pickup_time):
        global WAITING_QUEUE_TIME, LAST_QUEUE_UPDATE
        timeout = get_waiting_time(machine_settings)
        prio = get_priority_value_based_on_strategy(timeout, self.env.now, order_of_burger_pickup_time)

        if len(self.machine_four.queue) > 0:
            if LAST_QUEUE_UPDATE["M4"] is None:
                LAST_QUEUE_UPDATE["M4"] = self.env.now


        with self.machine_four.request(priority=prio) as request:
            yield request  

            if len(self.machine_four.queue) == 0:
                if LAST_QUEUE_UPDATE["M4"] is not None:  
                    WAITING_QUEUE_TIME["M4"] += self.env.now - LAST_QUEUE_UPDATE["M4"]
                LAST_QUEUE_UPDATE["M4"] = None

            OCCUPANCY_RATE["M4"] += timeout
            yield self.env.timeout(timeout)


    def machine_five_process(self, machine_settings, order_of_burger_pickup_time):
        global WAITING_QUEUE_TIME, LAST_QUEUE_UPDATE
        timeout = get_waiting_time(machine_settings)
        prio = get_priority_value_based_on_strategy(timeout, self.env.now, order_of_burger_pickup_time)

        if len(self.machine_five.queue) > 0:
            if LAST_QUEUE_UPDATE["M5"] is None:
                LAST_QUEUE_UPDATE["M5"] = self.env.now


        with self.machine_five.request(priority=prio) as request:
            yield request  

            if len(self.machine_five.queue) == 0:
                if LAST_QUEUE_UPDATE["M5"] is not None:  
                    WAITING_QUEUE_TIME["M5"] += self.env.now - LAST_QUEUE_UPDATE["M5"]
                LAST_QUEUE_UPDATE["M5"] = None

            OCCUPANCY_RATE["M5"] += timeout
            yield self.env.timeout(timeout)


def get_waiting_time(machine_setting):
    if machine_setting[1] == 'normal':
        return max(0, norm.rvs(loc=machine_setting[2], scale=machine_setting[3]))
    elif machine_setting[1] == 'exponential':
        return random.expovariate(machine_setting[2])
    elif machine_setting[1] == 'uniform':
        return random.uniform(machine_setting[2], machine_setting[3])
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
        time_between_orders = random.expovariate((1/90))
        yield env.timeout(time_between_orders)

        order_of_burger = Order(env)
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
    for burger_type, times in BURGER_THROUGHPUT_TIMES.items():
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            print(f"Burgertyp: {burger_type} ({len(times)}-mal hergestellt)")
            print(f"  Durchschnittliche Durchlaufzeit: {avg_time:.2f} Sekunden")
            print(f"  Maximale Durchlaufzeit: {max_time:.2f} Sekunden")
            print(f"  Minimale Durchlaufzeit: {min_time:.2f} Sekunden")
        else:
            print(f"Burgertyp: {burger_type} hat keine Durchlaufzeiten.")

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

def get_priority_value_based_on_strategy(value, timestamp, earliest_due_date):
    if STRATEGY == "FIFO":
        return timestamp

    if STRATEGY == "LIFO":
        return -timestamp

    if STRATEGY == "SPT":
        return value

    if STRATEGY == "LPT":
        return -value

    if STRATEGY == "RANDOM":
        return random.random()

    if STRATEGY == "EDD":
        return earliest_due_date


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

    calculate_average_waiting_queue_time()
    save_average_waiting_queue_time(OUTPUT_FOLDER, "average_waiting_queue_time.csv", TOTAL_WAITING_QUEUE_TIME)
    save_average_throughput_times(OUTPUT_FOLDER, "throughput_times.csv", TOTAL_BURGER_THROUGHPUT_TIMES)