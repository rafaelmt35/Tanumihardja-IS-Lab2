import random as rand
import string

cyrillic_letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
punctutation_marks = " .,?!/"

class Individual:
    def get_genes(self):
        return self.genes

    def get_fitness(self):
        return self.fitness_score

    def fitness(self, target):
        score = 0
        for char_genes, char_target in zip(self.genes, target):
            if (char_genes == char_target):
                score += 1
        self.fitness_score = score / self.length

    def crossover(self, parent_a, parent_b, mid_point):
        genes_a = parent_a.get_genes()
        genes_b = parent_b.get_genes()
        self.genes = genes_a[:mid_point] + genes_b[mid_point:]

    def mutation(self, mutation_rate):
        for item in self.genes:
            if rand.uniform(0.00, 1.00) < mutation_rate:
                item = self.get_char()

    def get_char(self):
        return rand.choice(cyrillic_letters + string.ascii_letters + punctutation_marks)

    def __init__(self, length):
        self.length = length
        self.genes = ''.join(self.get_char() for _ in range(self.length))
        self.fitness_score = 0
