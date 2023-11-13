import pandas as pd
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value


# Select topN Liquidity from dataset
def data_top(path, n):
  df_all = pd.read_csv(path)
  df_sorted = df_all.sort_values(by='Liquidity', ascending=False)
  top_rows = df_sorted.head(n)
  return top_rows

def df2lists(df):
  Symbol = df['Symbol'].tolist()
  P = df['Lastest Price'].tolist()
  ER = df['Expected Return'].tolist()
  R = df['Risk'].tolist()
  L = df['Liquidity'].tolist()
  return Symbol, P, ER, R, L

def ipSolve(Symbol, P, ER, R, L, budget):
  num_assets = len(Symbol)

  # Create the optimization problem
  model = LpProblem(name="Portfolio_Optimization", sense=LpMaximize)

  # Define decision variables (integer variables for asset selection)
  assets = range(len(Symbol))
  x = LpVariable.dicts("Asset", assets, lowBound=0, upBound=15, cat='Integer')

  # Define the objective function
  model += lpSum(ER[i] * x[i] * P[i] * 50 for i in assets), "Total_Return"

  # Define the constraints
  model += lpSum(x[i] * P[i] * 50 for i in assets) <= budget, "Budget_Constraint"


  # Solve the optimization problem
  model.solve()

  # Print the solution status
  # print("Status:", model.status)

  # Print the selected assets and their fractions
  selected_x = [value(x[i]) for i in assets]
  opt_x = [element * 100 for element in selected_x]
  print("Number of shares in each Assets:", opt_x)

  # Print the optimized total return
  optimized_return = value(model.objective)
  print("Optimized Total Return:", optimized_return)

  # Print the values of constraints
  for name, constraint in model.constraints.items():
    print(f"{name}: {value(constraint)}")


  return selected_x, optimized_return

# Read and select top data
def main(path, n, budget):
  df = data_top(path, n)
  print(df)
  Symbol, P, ER, R, L = df2lists(df)
  selected_x, optimized_return = ipSolve(Symbol, P, ER, R, L, budget)
  

path = 'Symbols45.csv'
main(path, 45, 1000000)
