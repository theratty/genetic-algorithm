#!/usr/bin/env python3
import random
from geneticalgorithm import GeneticAlgorithm
from helper import FileHandler
from helper import GeneticOperatorProvider
from helper import GaImprover

class Application:
    def __init__(self):
        self.file_handler = FileHandler()
        self.genetic_operator_provider = GeneticOperatorProvider()
        self.ga_improver = GaImprover()

        self.path_to_input_file = "maleplyty.txt"
        self.path_to_output_file = "output.txt"
        self.path_to_output_png = "output.png"

    def prepare_data_for_ga(self, original_data):
        data_for_ga = []
        for idx, element in enumerate(original_data):
            single_board = {}
            single_board["board_no"] = idx
            single_board["width"] = element[0]
            single_board["height"] = element[1]
            data_for_ga.append(single_board)

        return data_for_ga

    def run(self):
        input_data = self.file_handler.read_data(self.path_to_input_file)
        data_for_ga = self.prepare_data_for_ga(input_data)

        ga = GeneticAlgorithm(seed_data = data_for_ga,
                              verbose = True,
                              ga_improver = self.ga_improver)

        ga.create_individual = self.genetic_operator_provider.get_create_individual()
        ga.mutate_function = self.genetic_operator_provider.get_mutate()

        if len(data_for_ga) > 2:
            ga.crossover_function = self.genetic_operator_provider.get_double_crossover()
        elif len(data_for_ga) == 2:
            ga.crossover_function = self.genetic_operator_provider.get_crossover()
        else:
            ga.crossover_function = self.genetic_operator_provider.get_no_crossover()

        self.genetic_operator_provider.set_tournament_size(10)
        ga.selection_function = self.genetic_operator_provider.get_selection()

        one_power_range = 20
        punish_powers = [1.033, 1.066, 1.1, 1.15, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.85]

        self.ga_improver.set_fitness_power_punish(power=1)
        ga.create_first_generation()
        for _ in range(2, one_power_range + 1):
            ga.create_next_generation()

        for power in punish_powers:
            self.ga_improver.set_fitness_power_punish(power=power)
            for _ in range(1, one_power_range + 1):
                ga.create_next_generation()

        self.ga_improver.set_fitness_no_mercy()
        for _ in range(1, one_power_range + 1):
            ga.create_next_generation()

        best = ga.best_individual()

        self.file_handler.save_data_as_txt(self.path_to_output_file, best, data_for_ga)
        self.file_handler.save_data_as_png(self.path_to_output_png, best, data_for_ga)


if __name__ == "__main__":
    a = Application()
    a.run()
