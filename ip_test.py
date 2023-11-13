from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value

# Sample data (replace this with your own data)
Symbol = ['HDFC', 'BRITANNIA', 'BAJFINANCE', 'ASIANPAINT', 'HINDUNILVR', 'ULTRACEMCO']
P = [2420.1, 3449, 5451.9, 2536.4, 2353.75, 6278.95]    # price
ER = [0.0832, 0.080, 0.2750, 0.0815, 0.0150, 0.1851]    # expected return
R = [0.0845, 0.1817, 0.491, 0.1226, 0.0905, 0.0853]     # risk
L = [0.6531, 0.6445, 0.6279, 0.6256, 0.6032, 0.6019]    # liquidity

budget = 1000000
num_assets = len(Symbol)

# Create the optimization problem
model = LpProblem(name="Portfolio_Optimization", sense=LpMaximize)

# Define decision variables (binary variables for asset selection)
assets = range(len(Symbol))
x = LpVariable.dicts("Asset", assets, lowBound=0, upBound=None, cat='Integer')

# Define the objective function
model += lpSum(ER[i] * x[i] * P[i] * 100 for i in assets), "Total_Return"

# Define the constraints
model += lpSum(x[i] * P[i] * 100 for i in assets) <= budget, "Budget_Constraint"
model += lpSum(x[i] * P[i] for i in assets) <= 0.7*budget, "Diversity1_Constraint"
# model += x * P <= budget*0.7, "Diversity1_Constraint"

# Solve the optimization problem
model.solve()

# Print the solution status
# print("Status:", model.status)

# Print the selected assets and their fractions
selected_x = [value(x[i]) for i in assets]
# print('Type value(x): ', type(value(x[i]) for i in assets))
opt_x = [element * 100 for element in selected_x]
print("Number of shares in each Assets:", opt_x)

# Print the optimized total return
optimized_return = value(model.objective)
print("Optimized Total Return:", optimized_return)

# Print the values of constraints
for name, constraint in model.constraints.items():
    print(f"{name}: {value(constraint)}")