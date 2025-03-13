import pandas as pd

# Read the CSV with low_memory=False to avoid DtypeWarning
df = pd.read_csv("sp500.csv", low_memory=False)

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Calculate unique tickers
unique_tickers = df['TICKER'].nunique()

# Get min and max dates
min_date = df['date'].min()
max_date = df['date'].max()

print(f"Number of unique tickers: {unique_tickers}")
print(f"Minimum date: {min_date.strftime('%Y-%m-%d')}")
print(f"Maximum date: {max_date.strftime('%Y-%m-%d')}")