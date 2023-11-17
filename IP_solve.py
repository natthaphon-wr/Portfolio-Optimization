import pandas as pd
import matplotlib.pyplot as plt
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value
from pulp.apis import PULP_CBC_CMD


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
def solver_single(Symbol, P, ER, R, L, budget):
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
  model += lpSum(x[i] * P[i] * R[i] for i in assets)/budget <= 0.2, "Risk_Constraint"
  for i in assets:
    model += (x[i] * P[i])/budget <= 0.7, f"Diversity_{i}_Constraint"

  # Solve the optimization problem
  model.solve(PULP_CBC_CMD(msg=False))
  # model.solve()

  # Print the solution status
  # print("Status:", model.status)

  # Print the values of constraints
  # for name, constraint in model.constraints.items():
  #   print(f"{name}: {value(constraint)}")

  # Result: Symbol and Number of shares to invest
  result_col = ['Symbol', 'Price', 'NumberShares', 'Expected Return', 'Risk']
  result_df = pd.DataFrame(columns=result_col)
  for i in assets:
    if value(x[i]) > 0:
      new_data = pd.DataFrame([[Symbol[i], P[i], value(x[i]), ER[i], R[i]]], columns=result_col)
      result_df = pd.concat([result_df, new_data], ignore_index=True)

  # Print the optimized total return
  optimized_return = value(model.objective)

  return result_df, optimized_return

# Read and select top data
def main_single(path, n, budget):
  df = data_top(path, n)
  Symbol, P, ER, R, L = df2lists(df)
  result_df, optimized_return = solver_single(Symbol, P, ER, R, L, budget)
  total_invest = (result_df['Price'] * result_df['NumberShares']).sum()

  return result_df, total_invest, optimized_return

# Called main function
# Finally, use Symbols27 file with eliminate liquid with less than 0.5.
#   Largest problem is using 27 symbols
#   Medium problem is using 20 symbols that selected symbols with top20 liquidity 
#   Smallest problem is using 10 symbols that selected symbols with top10 liquidity 
def main():
  path = 'Symbols24.csv'

  # Small problem
  result_12, totalInvest_12, optReturn_12 = main_single(path, 12, 1000000)
  print('\nSmall problem with 12 considered symbols')
  print(result_12)
  print('Total Investment: ', totalInvest_12)
  print("Optimized Total Return:", optReturn_12)

  # # Medium problem
  # result_15, totalInvest_15, optReturn_15 = main_single(path, 15, 1000000)
  # print('\nMedium problem with 20 considered symbols')
  # print(result_15)
  # print('Total Investment: ', totalInvest_15)
  # print("Optimized Total Return:", optReturn_15)

  # Large problem
  result_24, totalInvest_24, optReturn_24 = main_single(path, 24, 1000000)
  print('\nLarge problem with 24 considered symbols')
  print(result_24)
  print('Total Investment: ', totalInvest_24)
  print("Optimized Total Return:", optReturn_24)


main()
# top_rows = data_top('Symbols27.csv', 27)

