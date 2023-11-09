import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = 'opt_dataset.csv' 

df = pd.read_csv(csv_file_path)

condition = (df['Expected Return'] > 0) & (df['Lastest Price'] <= 10000) & (df['Lastest Price'] >= 1000) & (df['Liquidity'] >= 0.6) 
filtered_df = df[condition]
print("Filtered Data:")
print(filtered_df)
print("Number of considering stock: ", len(filtered_df))

# Save new df to csv file
file_path = 'Symbols6.csv'  # Set the file path and name
filtered_df.to_csv(file_path, index=False)

