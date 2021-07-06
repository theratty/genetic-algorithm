import random
import copy
from operator import attrgetter
import threading
import math
from .chromosome import Chromosome

from six.moves import range


class GeneticAlgorithm(object):
    def __init__(self,
                 seed_data,
                 population_size=1200,
                 generations=260,
                 crossover_probability=0.8,
                 mutation_probability=0.3,
                 elitism=True,
                 maximise_fitness=True,
                 verbose=False,
                 elite_selection=0.005,
                 ga_improver=None):

        self.seed_data = seed_data
        self.population_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.elitism = elitism
        self.maximise_fitness = maximise_fitness
        self.verbose = verbose
        self.generation_no = 0
        self.ga_improver = ga_improver
        self.elite_selection = elite_selection

        self.current_generation = []
        self.fitness_function = None
        self.random_selection = None
        self.create_individual = None
        self.crossover_function = None
        self.mutate_function = None
        self.selection_function = None

    def create_initial_population(self):
        initial_population = []
        for _ in range(self.population_size):
            genes = self.create_individual(self.seed_data)
            individual = Chromosome(genes)
            initial_population.append(individual)
        self.current_generation = initial_population

    def one_thread_task(self, begin, end):
        for idx in range(begin, end):
            individual = self.current_generation[idx]
            individual.fitness = self.ga_improver.current_fitness_function(individual.genes, self.seed_data)

    def calculate_population_fitness(self):
        begin = 0
        one_thread_range = len(self.current_generation) // self.ga_improver.fitness_threads_no
        thread_list = []

        while begin < len(self.current_generation):
            end = begin + one_thread_range
            thread = threading.Thread(target=self.one_thread_task, args=(begin, end))
            thread_list.append(thread)
            begin += one_thread_range
            
        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

    def rank_population(self):
        self.current_generation.sort(key=attrgetter('fitness'), reverse=self.maximise_fitness)

    def create_new_population(self):
        new_population = []
        elite_size = math.floor(len(self.current_generation) * self.elite_selection)
        elite = copy.deepcopy(self.current_generation[0:elite_size])
        selection = self.selection_function

        while len(new_population) < self.population_size:
            parent_1 = copy.deepcopy(selection(self.current_generation))
            parent_2 = copy.deepcopy(selection(self.current_generation))

            child_1, child_2 = parent_1, parent_2
            child_1.fitness, child_2.fitness = 0, 0

            can_crossover = random.random() < self.crossover_probability
            can_mutate = random.random() < self.mutation_probability

            if can_crossover:
                child_1.genes, child_2.genes = self.crossover_function(
                    parent_1.genes, parent_2.genes)

            if can_mutate:
                self.mutate_function(child_1.genes)
                self.mutate_function(child_2.genes)

            new_population.append(child_1)
            if len(new_population) < self.population_size:
                new_population.append(child_2)

        if self.elitism:
            for idx, el in enumerate(elite):
                new_population[idx] = el

        self.current_generation = new_population

    def create_first_generation(self):
        self.generation_no += 1
        self.create_initial_population()
        self.calculate_population_fitness()
        self.rank_population()
        
        if self.verbose:
            print("Generation: %d - Best Fitness: %f" % (self.generation_no, self.best_individual()[0]))

    def create_next_generation(self):
        self.generation_no += 1
        self.create_new_population()
        self.ga_improver.improve_population(self.current_generation, self.seed_data, self.generation_no)
        self.calculate_population_fitness()
        self.rank_population()
        
        if self.verbose:
            print("Generation: %d - Best Fitness: %f" % (self.generation_no, self.best_individual()[0]))

    def best_individual(self):
        best = self.current_generation[0]
        return (best.fitness, best.genes)
