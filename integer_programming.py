import pandas as pd
import matplotlib.pyplot as plt
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value


# Select topN Liquidity from dataset
def data_top(path, n):
  df_all = pd.read_csv(path)
  df_sorted = df_all.sort_values(by='Liquidity', ascending=False)
  top_rows = df_sorted.head(n)
  return top_rows

# Create lists of each feature from df
def df2lists(df):
  Symbol = df['Symbol'].tolist()
  P = df['Lastest Price'].tolist()
  ER = df['Expected Return'].tolist()
  R = df['Risk'].tolist()
  L = df['Liquidity'].tolist()
  return Symbol, P, ER, R, L

# Solving the problem with pulp
def ipSolve(Symbol, P, ER, R, L, budget):
  # Create the optimization problem
  model = LpProblem(name="Portfolio_Optimization", sense=LpMaximize)

  # Define decision variables (integer variables for asset selection)
  assets = range(len(Symbol))
  x = LpVariable.dicts("Asset", assets, lowBound=0, upBound=1000, cat='Integer')
  y = LpVariable.dicts("Asset_select", assets, cat='Binary')

  # Define the objective function
  model += lpSum(ER[i] * x[i] * P[i] for i in assets), "Total_Return"

  # Define the constraints
  model += lpSum(x[i] * P[i] for i in assets) <= budget, "Budget_Constraint"
  for i in assets:
    model += (x[i] * P[i])/budget <= 0.7, f"Diversity_{i}_Constraint"

  # Solve the optimization problem
  model.solve()

  # Print the solution status
  # print("Status:", model.status)

  # Print the values of constraints
  # for name, constraint in model.constraints.items():
  #   print(f"{name}: {value(constraint)}")

  # Result: Symbol and Number of shares to invest
  result_col = ['Symbol', 'Price', 'NumberShares', 'Liquidity']
  result_df = pd.DataFrame(columns=result_col)
  for i in assets:
    if value(x[i]) > 0:
      new_data = pd.DataFrame([[Symbol[i], P[i], value(x[i]), L[i]]], columns=result_col)
      result_df = pd.concat([result_df, new_data], ignore_index=True)

  # Print the optimized total return
  optimized_return = value(model.objective)

  return result_df, optimized_return

# Read and select top data
def main(path, n, budget):
  df = data_top(path, n)
  Symbol, P, ER, R, L = df2lists(df)
  result_df, optimized_return = ipSolve(Symbol, P, ER, R, L, budget)
  total_invest = (result_df['Price'] * result_df['NumberShares']).sum()
  print(result_df)
  print('Total Investment: ', total_invest)
  print("Optimized Total Return:", optimized_return)


# Called main function
# Finally, use Symbols27 file with eliminate liquid with less than 0.5.
#   Largest problem is using 27 symbols
#   Medium problem is using 20 symbols that selected symbols with top20 liquidity 
#   Smallest problem is using 10 symbols that selected symbols with top10 liquidity 
path = 'Symbols27_elimLiquid.csv'
main(path, 27, 1000000)
