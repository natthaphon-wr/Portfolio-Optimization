import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpStatus


# Select topN Liquidity from dataset
def data_top(path, n):
  df_all = pd.read_csv(path)
  df_sorted = df_all.sort_values(by='Liquidity', ascending=False)
  top_rows = df_sorted.head(n)
  return top_rows

# Solving single objective problem 
def lp_problem(df, budget):
  # Extract data from df
  # n = len(df)
  # series_from_index = df.reset_index()['index']
  # print(series_from_index)

  # USE ORIGINAL INDEX AS INDEX

  # Define information variables (pd.series)
  S = df['Symbol']
  P = df['Lastest Price']
  ER = df['Expected Return'] 
  R = df['Risk']
  L = df['Liquidity']

  # # Create the ILP problem
  # problem = LpProblem("IntegerProgrammingExample", LpMaximize)

  # # Define decision variables
  # X = {i: LpVariable(name=f"x_{i}", cat="Binary") for i in S.index}

  # # Define derived variables


  # # Define the objective function
  # prob += lpSum(ER[i] * ( X[i] ) for i in S.index), "Objective"

  # # Define constraints
  # for i in P.index:
  #     prob += lpSum(X[i] * P[i] * 100  for i in P.index) <= budget


  # # Solve the ILP problem
  # prob.solve()

  # # Print the solution status
  # print("Status:", LpStatus[prob.status])


def lp_problem_dummy(df, budget):
  # Define information variables
  n = len(df)
  series_from_index = df.reset_index()['index']
  S = df['Symbol'].tolist()
  P = df['Lastest Price'].tolist()
  ER = df['Expected Return'].tolist()
  R = df['Risk'].tolist()
  L = df['Liquidity'].tolist()


  # Create a LP problem
  problem = LpProblem("Portfolio_Optimization", LpMaximize)

  # Define decision variables
  # X = [LpVariable(name=f"x_{i}", cat="Integer", lowBound=0, upBound=7) for i in range(n)]
  X = {stock: LpVariable(f"Shares_{stock}", lowBound=0, upBound=7, cat='Integer') for stock in S}

  # Define derived variables
  # Y = [1 if value > 1 else 0 for value in X]
  total_price = lpSum(x * p for x, p in zip(X, P))
  W = (x * p for x, p in zip(X, P))/total_price

  # W = (x * p for x, p in zip(X, P)) / (sum(x * p for x, p in zip(X, P)))

  # Define the objective function
  problem += lpSum(ER[stock] * W[stock] for stock in S), "Expected_Portfolio_Return"


  # Define constraints
  # 1. Price constraints
  for i in range(len(P)):
    problem += lpSum(P[i][j] * X[j] for j in range(n)) <= budget
  # 2. At least 3 symbols
  # problem += lpSum(Y[i] for i in range(n)) >= 3
  

  # Solve the ILP problem
  problem.solve()

  # Print the status of the solution
  print("Status:", LpStatus[problem.status])

  # Print the optimized portfolio
  if LpStatus[problem.status] == "Optimal":
      print("\nOptimal Portfolio:")
      for stock in S:
          print(f"{stock}: {X[stock].value()} shares")
  else:
      print("No optimal solution found.")


# Test PuLP
def test_PuLP():
  # Create a LP problem
  problem = LpProblem("IntegerProgrammingExample", LpMaximize)

  # Define decission variable
  x1 = LpVariable("x1", lowBound=0, upBound=7, cat="Integer") 
  x2 = LpVariable("x2", lowBound=0, upBound=7, cat="Integer") 

  # Set up the objective function
  problem += 5 * x1 + 3 * x2, "Objective"

  # Add constraints
  problem += 2 * x1 + x2 <= 8, "Constraint_1"
  problem += 4 * x1 - 5 * x2 >= -5, "Constraint_2"
  problem += x1 + 2 * x2 <= 5, "Constraint_3"

  # Solve the problem
  problem.solve()

  # Print the results
  print("Status:", problem.status)
  print("Objective Value:", round(problem.objective.value(), 2))

  for variable in problem.variables():
      print(f"{variable.name} = {round(variable.value(), 2)}")



# Read and select top data
df_all = pd.read_csv('opt_dataset.csv')
path = 'opt_dataset.csv'
df = data_top(path, 6)
# print(df)

budget = 1000000
lp_problem_dummy(df, budget)
