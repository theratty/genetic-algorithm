import random
from .helper_functions import *
from operator import attrgetter

class GeneticOperatorProvider:
    def __init__(self):

        def create_individual(seed_data):
            individual = []
            for el in seed_data:
                signle_board = {}
                signle_board["x"] = random.randint(0, BIG_BOARD_WIDTH - 1)
                signle_board["y"] = random.randint(0, BIG_BOARD_HEIGHT - 1)
                signle_board["r"] = random.randint(0, 1)
                signle_board["e"] = random.randint(0, 1)
                individual.append(signle_board)

            return individual
        
        def no_corssover(parent_1, parent_2):
            child_1 = parent_1
            child_2 = parent_2
            return child_1, child_2

        def crossover(parent_1, parent_2):
            index = random.randrange(1, len(parent_1))
            child_1 = parent_1[:index] + parent_2[index:]
            child_2 = parent_2[:index] + parent_1[index:]
            return child_1, child_2

        def double_crossover(parent_1, parent_2):
            index1 = random.randrange(1, len(parent_1) - 1)
            index2 = random.randrange(index1, len(parent_1))
            child_1 = parent_1[:index1] + parent_2[index1:index2] + parent_1[index2:]
            child_2 = parent_2[:index1] + parent_1[index1:index2] + parent_2[index2:]
            return child_1, child_2

        def mutate(individual):
            el_to_mutate = random.randint(0, 3)
            index = random.randrange(0, len(individual))

            if el_to_mutate == 0:
                individual[index]["x"] = random.randint(0, BIG_BOARD_WIDTH - 1)
            elif el_to_mutate == 1:
                individual[index]["y"] = random.randint(0, BIG_BOARD_HEIGHT - 1)
            elif el_to_mutate == 2:
                individual[index]["r"] = random.randint(0, 1)
            else:
                individual[index]["e"] = random.randint(0, 1)

            return individual

        self.tournament_size = 0

        def tournament_selection(population):
            if self.tournament_size == 0:
                self.tournament_size = 2
            members = random.sample(population, self.tournament_size)
            members.sort(key=attrgetter('fitness'), reverse=True)

            return members[0]

        self.create_individual = create_individual
        self.no_corssover = no_corssover
        self.crossover = crossover
        self.double_crossover = double_crossover
        self.mutate = mutate
        self.selection = tournament_selection

    def set_tournament_size(self, size):
        self.tournament_size = size

    def get_selection(self):
        return self.selection

    def get_create_individual(self):
        return self.create_individual

    def get_no_crossover(self):
        return self.no_corssover

    def get_crossover(self):
        return self.crossover

    def get_double_crossover(self):
        return self.double_crossover

    def get_mutate(self):
        return self.mutate
                    
