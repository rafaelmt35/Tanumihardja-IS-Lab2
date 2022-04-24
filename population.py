import random as rand
from individual import Individual


class Population:
    def calc_fitness(self):
        self.population_fitness.clear()
        for individual in self.population:
            individual.fitness(self.target)
            self.population_fitness.append(individual.get_fitness())

        self.max_fitness = self.get_max_fitness()
        self.average_fitness = self.get_average_fitness()

    def get_average_fitness(self):
        return sum(self.population_fitness) / len(self.population_fitness)

    def get_max_fitness(self):
        max = 0
        for fitness in self.population_fitness:
            if fitness > max:
                max = fitness
        return max

    def natural_selection(self):
        self.selected = []
        for _ in range(self.number_of_population):
            self.selected.append(self.acept_reject())

    def acept_reject(self):
        # If none of the generated genes have the same dna with our target  (max_fitness = 0)
        # just add random individual into the selected array
        if not self.max_fitness > 0:
            index = rand.randrange(len(self.population_fitness))
            return self.population[index]
        count = 0
        while(True and count < 10000):
            index = rand.randrange(len(self.population_fitness))
            individual_fitness = self.population_fitness[index]
            r = rand.random()
            if (r <= individual_fitness):
                return self.population[index]
            count += 1

    def generate_generation(self):
        new_generation = []
        new_generation_genes = []
        for i in range(self.number_of_population):
            # Pick a random integer value to determine the parent for crossing / breeding
            a = rand.randrange(len(self.selected))
            b = rand.randrange(len(self.selected))

            parent_a = self.selected[a]
            parent_b = self.selected[b]

            # Create child individual. Since crossover can obtained 2 child here we create 2 child individual.
            child1 = Individual(len(self.target))
            child2 = Individual(len(self.target))

            # Get the middle point for crossover
            n = rand.randrange(len(self.target))

            # Crossover the genetics from parent A and B.
            # First n - 1 genes from partnerA and last n genes from partnerB are taken then combined.
            # Ex: n = 3
            # A = [a,b,c,d,e]
            # B = [z,x,c,v,b]
            # child = [a,b,c,v,b]
            child1.crossover(parent_a, parent_b, n)

            # First n - 1 genes from partnerB and last n genes from partnerA are taken then combined.
            # Ex: n = 3
            # A = [a,b,c,d,e]
            # B = [z,x,c,v,b]
            # child = [z,x,c,d,e]
            child2.crossover(parent_b, parent_a, n)

            # Mutate some of child the genes based on the mutation rate
            child1.mutation(self.mutation_rate)

            child2.mutation(self.mutation_rate)

            # To get the most unique genes among the child
            if child1.get_genes() not in new_generation_genes:
                new_generation.append(child1)
                new_generation_genes.append(child1.get_genes())
            if child2.get_genes() not in new_generation_genes:
                new_generation.append(child2)
                new_generation_genes.append(child2.get_genes())

        self.generations += 1

        # Constraints if the number of unique child/new generation is less than the number of population, repopulate
        # the population with the new generation and pick random n individual from the previous population
        # Else if the number of new generation is the same or bigger then pick number of population individual from the
        # new generation.
        if len(new_generation) < self.number_of_population:
            self.population = new_generation + \
                list(rand.sample(self.population,
                     self.number_of_population - len(new_generation)))
        else:
            self.population = list(rand.sample(
                new_generation, self.number_of_population))

    def get_population(self):
        populations = []
        for individual in self.population:
            populations.append(individual.Get_Genes())
        return populations

    def get_best_individual(self):
        best_genes = ""
        best_fit = 0.00
        for individual in self.population:
            if individual.get_fitness() > best_fit:
                best_fit = individual.get_fitness()
                best_genes = individual.get_genes()

        if best_genes == self.target:
            self.matching_genes = True

        return best_genes

    def reach_target(self):
        return self.matching_genes

    def current_generations(self):
        print(f"Generation #{self.generations}\n")
        print(f"The current best matching genes: {self.get_best_individual()}\n")
        print(f"Total current population: {len(self.population)}\n")
        print(f"Average current fitness: {round(self.average_fitness * 100, 2)} %\n")
        print(f"Max current fitness: {round(self.max_fitness * 100, 2)} %\n")
        print(f"Mutation rate: {self.mutation_rate * 100} %\n\n")
        return {
            "generation": self.generations,
            "best_genes": self.get_best_individual(),
            "total_population": len(self.population),
            "average_fitness": round(self.average_fitness * 100, 2),
            "max_fitness": round(self.max_fitness * 100, 2),
            "mutation_rate": self.mutation_rate * 100
        }

    def __init__(self, target, n, mutation_rate):
        self.population = []
        self.number_of_population = n
        self.target = target
        self.mutation_rate = mutation_rate
        self.matching_genes = False
        self.population_fitness = []
        self.generations = 1
        self.max_fitness = 0
        self.average_fitness = 0

        for _ in range(self.number_of_population):
            self.population.append(Individual(len(self.target)))

        self.selected = []
