class Chromosome(object):
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0

    def __repr__(self):
        return repr((self.fitness, self.genes))