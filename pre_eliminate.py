import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = 'opt_dataset.csv' 

df = pd.read_csv(csv_file_path)

condition = (df['Liquidity'] >= 0.5) & (df['Liquidity'] <= 0.8)
filtered_df = df[condition]
df_sorted = filtered_df.sort_values(by='Liquidity', ascending=False)
print("Filtered Data:")
print(df_sorted)
print("Number of considering stock: ", len(df_sorted))

# Save new df to csv file
file_path = 'Symbols27.csv'  # Set the file path and name
df_sorted.to_csv(file_path, index=False)

