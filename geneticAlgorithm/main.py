import random

from engine.engine import Engine


def splitter(array, partsize=1):
    return [array[i:i+partsize] for i in range(0, len(array), partsize)]


def is_solution(node):
    equation = '{} and ({} or {}) and {}'.format(*node['cromossome'])
    return eval(equation)


def mutate(node):
    index = random.randint(0, len(node['cromossome'])-1)
    node['cromossome'][index] = random.randint(0, 1)
    return node


def crossover(node1, node2):
    cromo1 = node1['cromossome']
    cromo2 = node2['cromossome']

    nu_cromo = cromo1[:len(cromo1)//2] + cromo2[len(cromo2)//2:]
    return {'cromossome': nu_cromo}


def fitness(node):
    cromo = node['cromossome']
    fit = 0

    if sum(cromo) == 0:
        fit = 0

    if sum(cromo) == 1:
        fit = .2

    if sum(cromo) == 2:
        fit = .4

    if cromo[0] == 1 and cromo[1] == 0 and cromo[2] == 1 and cromo[3] == 0:
        fit = .5

    if cromo[0] == 0 and cromo[1] == 1 and cromo[2] == 0 and cromo[3] == 1:
        fit = .5

    if cromo[0] == 1 and cromo[1] == 1:
        fit = .8

    if cromo[2] == 1 and cromo[3] == 1:
        fit = .8

    if cromo[0] == 1 and cromo[1] == 1 or cromo[2] == 1 and cromo[3] == 1:
        fit = 1

    node['fitness'] = fit
    return node


def prepared_crossover(population):
    return splitter(population, 2)


def quicksort(population):
    if len(population) <= 1:
        return population

    pivot = population[0]
    lesser = [i for i in population if i['fitness'] < pivot['fitness']]
    equal = [i for i in population if i['fitness'] == pivot['fitness']]
    greater = [i for i in population if i['fitness'] > pivot['fitness']]

    return quicksort(greater) + equal + quicksort(lesser)


def select_best(population):
    return quicksort(population)[:len(population)//2]


node1 = {
    'cromossome': [0, 0, 0, 0],
    'fitness': 0
}

node2 = {
    'cromossome': [1, 0, 0, 0],
    'fitness': 1
}

node3 = {
    'cromossome': [0, 0, 0, 1],
    'fitness': 2
}

engine = Engine(elitist_size=2, initital_population=[node1, node2, node3], max_iterations=100,
                is_solution_fun=is_solution, mutate_fun=mutate, crossover_fun=crossover,
                fitness_fun=fitness, prepared_crossover_fun=prepared_crossover, select_best_fun=select_best)
print(engine.execute())
