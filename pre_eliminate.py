import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = 'opt_dataset.csv' 

df = pd.read_csv(csv_file_path)

condition = (df['Liquidity'] >= 0.5) & (df['Liquidity'] <= 0.8) & (df['Expected Return'] <= 0.3) & (df['Lastest Price'] <= 10000) 
filtered_df = df[condition]
df_sorted = filtered_df.sort_values(by='Liquidity', ascending=False)

# Plot histrogram price
plt.hist(df_sorted['Lastest Price'])
plt.xlabel('Price')
plt.ylabel('Number of Stock Symbols')
plt.title('Histrogram of Price in Data')
plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
plt.show()

# Plot histrogram expected return
plt.hist(df_sorted['Expected Return'])
plt.xlabel('Expected Return')
plt.ylabel('Number of Stock Symbols')
plt.title('Histrogram of Expected Returna in Data')
plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
plt.show()

# Plot histrogram risk
plt.hist(df_sorted['Risk'])
plt.xlabel('Risk')
plt.ylabel('Number of Stock Symbols')
plt.title('Histrogram of Risk in Data')
plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
plt.show()

print("Filtered Data:")
print(df_sorted)
print("Number of considering stock: ", len(df_sorted))

# Save new df to csv file
# file_path = 'Symbols24.csv'  # Set the file path and name
# df_sorted.to_csv(file_path, index=False)

