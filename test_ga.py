import numpy as np
import pygad


# Data
function_inputs = [4,-2,3.5,5]
desired_output = 44

P = np.array([2420.1, 3449.0, 5451.9, 2536.4])
ER = np.array([0.0831, 0.0809, 0.2749, 0.0815])
R = np.array([0.0844, 0.1817, 0.4919, 0.1226])

# Fitness Function
def fitness_func(ga_instance, solution, solution_idx):
  output = np.sum(solution*function_inputs)
  fitness = 1.0 / np.abs(output - desired_output)
  return fitness

def fitness2(ga_instance, solution, solution_idx):
  # budget constraint
  if np.sum(solution*P) > 1000000:
    return 0
  
  # diversity constraint
  for i in range(len(P)):
    if solution[i]*P[i]/1000000 >= 0.7:
      return 0

  fitness = np.sum(solution*P*ER)  

  return fitness

# GA parameters
# num_generations = 100
# num_parents_mating = 4
# sol_per_pop = 8
# num_genes = len(function_inputs)
# init_range_low = 0
# init_range_high = 999
# parent_selection_type = "sss"
# keep_parents = 1
# crossover_type = "single_point"
# mutation_type = "random"
# mutation_percent_genes = 10

# PyGAD instance
ga_instance = pygad.GA(num_generations = 100,
                      sol_per_pop = 1000,
                      num_parents_mating = 50,
                      fitness_func = fitness2,
                      gene_type = int,
                      num_genes = len(P),
                      init_range_low = 0,
                      init_range_high = 999,
                      parent_selection_type = "sss",
                      crossover_type = "two_points")

# Run instance
ga_instance.run()

# Result
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
