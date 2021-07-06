from .helper_functions import *
import math

class GaImprover:
    def __init__(self, fitness_threads_no = 4, inprove_freq = 60):
        self.current_fitness_function = None
        if fitness_threads_no < 1:
            fitness_threads_no = 1
        self.fitness_threads_no = fitness_threads_no
        self.power = 1
        self.inprove_freq = inprove_freq

        def fitness_no_mercy(individual, data):
            fitness_value = 0
            for idx, el in enumerate(individual):
                if el["e"] == 1:
                    fitness_value = fitness_value + data[idx]["width"] * data[idx]["height"]

            if calc_full_overlapsing_sum(individual, data) > 0 or check_if_elements_protrutes(individual, data) > 0:
                fitness_value = 0

            return fitness_value

        self.fitness_no_mercy = fitness_no_mercy

        def fitness_power_punish(individual, data):
            fitness_value = 0
            for idx, el in enumerate(individual):
                if el["e"] == 1:
                    fitness_value = fitness_value + data[idx]["width"] * data[idx]["height"]
            
            fitness_value = fitness_value - calc_full_overlapsing_sum(individual, data, self.power)
            fitness_value = fitness_value - check_if_elements_protrutes(individual, data, self.power)
            
            if fitness_value < 0:
                fitness_value = 0

            return fitness_value

        
        self.fitness_power_punish = fitness_power_punish

    def set_fitness_no_mercy(self):
        self.current_fitness_function = self.fitness_no_mercy
    
    def set_fitness_power_punish(self, power = 1):
        self.power = power
        self.current_fitness_function = self.fitness_power_punish

    def fix_individual_to_left(self, individual, data):
        border = [-1] * BIG_BOARD_HEIGHT
        pos_array = []
        for idx, el in enumerate(individual):
            if el["e"] == 1:
                pos = {"idx" : idx, "x" : el["x"]}
                pos_array.append(pos)

        pos_array.sort(key=lambda i: i["x"])

        for el in pos_array:
            idx = el["idx"]
            y_begin = individual[idx]["y"]
            
            if individual[idx]["r"] == 0:
                width = data[idx]["width"]
                height = data[idx]["height"]
            else:
                height = data[idx]["width"]
                width = data[idx]["height"]

            y_end = y_begin + height - 1
            new_x = max(border[y_begin:y_end + 1]) + 1

            individual[idx]["x"] = new_x

            border[y_begin:y_end + 1] = [new_x + width - 1] * height

    
    def fix_individual_to_top(self, individual, data):
        border = [-1] * BIG_BOARD_WIDTH
        pos_array = []
        for idx, el in enumerate(individual):
            if el["e"] == 1:
                pos = {"idx" : idx, "y" : el["y"]}
                pos_array.append(pos)

        pos_array.sort(key=lambda i: i["y"])

        for el in pos_array:
            idx = el["idx"]
            x_begin = individual[idx]["x"]
            
            if individual[idx]["r"] == 0:
                width = data[idx]["width"]
                height = data[idx]["height"]
            else:
                height = data[idx]["width"]
                width = data[idx]["height"]

            x_end = x_begin + width - 1
            new_y = max(border[x_begin:x_end + 1]) + 1

            individual[idx]["y"] = new_y

            border[x_begin:x_end + 1] = [new_y + height - 1] * width

    def tetris(self, population, data):
        pop_size = len(population)
        num_to_fix = math.ceil(pop_size * 0.025)
        
        for idx in range(0, pop_size):
            if num_to_fix is 0:
                break
            
            individual = population[idx].genes
            if calc_full_overlapsing_sum(individual, data) > 0:
                continue

            num_to_fix -= 1

            self.fix_individual_to_top(individual, data)
            self.fix_individual_to_left(individual, data)
            self.fix_individual_to_top(individual, data)
            self.fix_individual_to_left(individual, data)

    def improve_population(self, population, data, generation_no):
        if generation_no % self.inprove_freq == 0:
            self.tetris(population, data)
            