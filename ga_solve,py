import numpy as np
import pandas as pd
import cvxpy as cp
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import pygad

#print("PyGAD version:", pygad.__version__)

# Select topN Liquidity from dataset
def data_top(path, n):
  df_all = pd.read_csv(path)
  df_sorted = df_all.sort_values(by='Liquidity', ascending=False)
  top_rows = df_sorted.head(n)
  return top_rows

# Create nparray of each feature from df
def df2nparray(df):
  Symbol = df['Symbol'].to_numpy()
  P = df['Lastest Price'].to_numpy()
  ER = df['Expected Return'].to_numpy()
  R = df['Risk'].to_numpy()
  L = df['Liquidity'].to_numpy()
  return Symbol, P, ER, R, L


def fitness(ga_instance, solution, solution_idx):
  budget = 1000000

  # budget constraint
  if np.sum(solution*P) > budget:
    return 0
  
  # diversity constraint
  for i in range(len(P)):
    if solution[i]*P[i]/budget >= 0.7:
      return 0

  fitness = np.sum(solution*P*ER)  

  return fitness


def ga_solve(param_list):
  # GA parameters
  num_gen = param_list[0]
  num_pop = param_list[1]
  num_x = param_list[2]
  low_bound = param_list[3]
  high_bound = param_list[4]
  elite = param_list[5]
  keep_par = param_list[6]  
  mutation = param_list[7]                

  # PyGAD instance
  ga_instance = pygad.GA(num_generations = num_gen,
                        num_parents_mating = num_x,
                        fitness_func = fitness,
                        sol_per_pop = num_pop,                      
                        gene_type = int,
                        num_genes = len(Symbol),
                        init_range_low = low_bound,
                        init_range_high = high_bound,
                        keep_parents = keep_par, 
                        keep_elitism = elite,           
                        mutation_probability = mutation,
                        parent_selection_type = "rank", #rank base for exploitation
                        #K_tournament = num_parTour,
                        crossover_type = "two_points")

  # Run instance
  ga_instance.run()

  # Result from GA
  # ga_instance.plot_fitness()
  best_solution, best_fitness, solution_idx = ga_instance.best_solution() #best solution in last population

  return best_solution, best_fitness


# Read and select top data
def main_opt(path, n, param_list):
  df = data_top(path, n)
  global Symbol, P, ER, R, L  #define as global variables
  Symbol, P, ER, R, L = df2nparray(df)

  best_solution, best_fitness = ga_solve(param_list)

  # Result: Symbol and Number of shares to invest
  result_col = ['Symbol', 'Price', 'NumberShares', 'Expected Return', 'Risk']
  result_df = pd.DataFrame(columns=result_col)
  for i in range(len(Symbol)):
    new_data = pd.DataFrame([[Symbol[i], P[i], best_solution[i], ER[i], R[i]]], columns=result_col)
    result_df = pd.concat([result_df, new_data], ignore_index=True)
  return result_df, best_fitness

  # return best_fitness


def main():
  path = 'Symbols23.csv'

  # Small problem with 12 considered symbols
  num_gen_s = 500
  num_pop_s = 1000
  num_x_s = round(num_pop_s*0.9)
  low_bound_s = 0
  high_bound_s = 150
  elite_s = round(num_pop_s*0.1) 
  keep_par_s = 0   
  mutation_s = 0.05                      

  param_list_s = [num_gen_s, num_pop_s, num_x_s, low_bound_s, high_bound_s, elite_s, keep_par_s, mutation_s]
  bf_list_s = []
  for i in range(10):
    result_df, best_fitness = main_opt(path, 12, param_list_s)
    bf_list_s.append(best_fitness)
    print(result_df)
  print(bf_list_s)


   # Large problem with 24 considered symbols
  num_gen_l = 500
  num_pop_l = 5000
  num_x_l = round(num_pop_l*0.9)
  low_bound_l = 0
  high_bound_l = 200
  elite_l = round(num_pop_l*0.1) 
  keep_par_l = 0   
  mutation_l = 0.05                      

  param_list_l = [num_gen_l, num_pop_l, num_x_l, low_bound_l, high_bound_l, elite_l, keep_par_l, mutation_l]
  bf_list_l = []
  # for i in range(1):
  #   best_fitness = main_opt(path, 24, param_list_l)
  #   bf_list_l.append(best_fitness)
  # print(bf_list_l)



main()
