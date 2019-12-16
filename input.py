# game environment parameters
width = 120
height = 120
block_length = 10
brainLayer = [32, 30, 3]  # neural network layers that act as brain of snake

# genetic algorithm parameter
population_size = 25
no_of_generations = 100
per_of_best_old_pop = 20.0  # percent of best performing parents to be included
per_of_worst_old_pop = 4.0  # percent of worst performing parents to be included
mutation_percent = 15.0
mutation_intensity = 0.15
