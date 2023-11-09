import pandas as pd
from scipy.stats import gmean
import scipy
import numpy as np
import os
import warnings 

# Settings the warnings to be ignored 
warnings.filterwarnings('ignore') 


# Read all files in a directory
def ReadAll(directory_path):
  df_all = pd.DataFrame(columns=['Symbol', 'Lastest Price', 'Expected Return', 'Risk', 'Liquidity'])

  # Iterate through files in the directory
  for filename in os.listdir(directory_path):
      if filename.endswith('.csv'):
          file_path = os.path.join(directory_path, filename)
          df = pd.read_csv(file_path)

          # check empty file before
          if not df.empty:
            df_summary = Preprocess(df, filename)
            df_all = pd.concat([df_all, df_summary], ignore_index=True)

  # Read metadata file to get industry
  df2 = pd.read_csv('Metadata\stock_metadata.csv')
  df_merge = pd.merge(df_all, df2[['Symbol','Industry']], on='Symbol', how='inner')
  print(df_merge)

  # Save to CSV
  df_merge.to_csv('opt_dataset.csv', index=False) 


# Extract data from a file
def Preprocess(df, filename):
  # Select useful column
  selected_columns = ['Date', 'Close', 'VWAP', '%Deliverble']
  df = df[selected_columns]
  df['Date'] = pd.to_datetime(df['Date']) #Warning
  # df.loc[:, 'Date'] = pd.to_datetime(df.loc[:, 'Date'])

  # Calculate Annual Return for ER and Risk
  annual_return, year_count = Annual_Return(df)

  # 1. Stock Symbols
  symbol = filename.split('.')[0]

  # 2. Lastest Price
  latest_date_index = df[['Date']].idxmax()
  last_price = df['Close'].iloc[latest_date_index].values[0]
  # print("Lastest Price: ", last_price)

  # 3. Expected Return
  ER = Cal_ER(annual_return)
  # print("Expected Return: ", ER)
  
  # 4. Risk
  risk = Cal_Risk(annual_return)
  # print("Risk: ", risk)
  
  # 5. Liquidity  
  liquidity = df[['%Deliverble']].mean().values[0]
  # print("Liquidity: ", liquidity)

  df_summary = pd.DataFrame({'Symbol': [symbol], 
                             'Lastest Price': [last_price], 
                             'Expected Return': [ER], 
                             'Risk': [risk], 
                             'Liquidity': [liquidity],
                             'Year_Count': [year_count]})

  return df_summary

# Determine VWAP yearly
def Annual_VWAP(df):
  df['Year'] = df['Date'].dt.year #Warning
  # df.loc[:, ('Year')] = df.loc[:, ('Date')].dt.year
  
  yearly_data = {}
  unique_years = df['Year'].unique()
  for year in unique_years:
      yearly_data[year] = df[df['Year'] == year].copy()

  list_vwap = []
  year_count = {}
  for year, data in yearly_data.items():
    if len(data) > 200: # have enough data in each year
      year_count[year] = len(data)
      column_means = data[['VWAP']].mean()
      list_vwap.append(column_means)

  return list_vwap, year_count

# Calculate annual return from annual vwap
def Annual_Return(df):
  annual_vwap, year_count = Annual_VWAP(df)
  list_return = []
  for i in range(1, len(annual_vwap)-1):
    # (Current year - Last year)/Last year
    return_rate = (annual_vwap[i]-annual_vwap[i-1])/(annual_vwap[i-1])
    list_return.append(return_rate)

  return list_return, year_count

# Calculate expected return from annual return
def Cal_ER(annual_return):
  # annual_return = Annual_Return(df)
  annual_result = [x + 1 for x in annual_return]
  expected_return = gmean(annual_result)-1 # Calculate by geometric mean minus 1
  return expected_return[0]

# Calculate risk from annual return
def Cal_Risk(annual_return):
  # annual_return = Annual_Return(df)
  risk = np.var(annual_return, ddof=1)  # ddof=1 specifies that it's a sample variance
  return risk

directory_path = 'NTFTY50'
ReadAll(directory_path)
