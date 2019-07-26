from engine import splitter


# noinspection PyMethodMayBeStatic
class Engine:
    def __init__(self, elitist_size, initital_population, max_iterations, is_solution_fun, mutate_fun, crossover_fun,
                 fitness_fun, prepared_crossover_fun, select_best_fun):

        self._mutate_fun = mutate_fun
        self._crossover_fun = crossover_fun
        self._fitness_fun = fitness_fun
        self._is_solution_fun = is_solution_fun
        self._prepared_crossover_fun = prepared_crossover_fun
        self._select_best_fun = select_best_fun

        self._initital_population = initital_population
        self._elitist_Size = elitist_size
        self._max_iterations = max_iterations

    def _fitness(self, node):
        return self._fitness_fun(node)

    def _fitness_many(self, nodes):
        return [self._fitness(i) for i in nodes]

    def _mutate(self, node):
        return self._mutate_fun(node)

    def _mutate_many(self, population):
        return [self._mutate(i) for i in population]

    def _crossover(self, node1, node2):
        return self._crossover_fun(node1, node2)

    def _crossover_many(self, population):
        return [self._crossover(*i) for i in self._prepared_crossover_fun(population) if len(i) == 2]

    def _is_solution(self, node):
        return self._is_solution_fun(node)

    def _get_solution(self, population):
        for i in population:
            if self._is_solution(i):
                return i

        return None

    def _build_population(self, mutated_best, offspring):
        return mutated_best + offspring

    def _generate_initial_pop(self):
        return self._initital_population

    def _select_best(self, population):
        return self._select_best_fun(population)

    def _apply_iteration(self, population=None, mutated=(), offspring=()):
        if population is None:
            return self._fitness_many(self._generate_initial_pop())

        return self._fitness_many(self._build_population(mutated, offspring))

    def execute(self):
        current_population = self._apply_iteration()
        for i in range(self._max_iterations):
            solution = self._get_solution(current_population)
            if solution is not None:
                return solution, i

            best_in_population = self._select_best(current_population)
            offspring = self._crossover_many(current_population)
            mutated = self._mutate_many(best_in_population)

            current_population = self._apply_iteration(current_population, mutated, offspring)

        return None
