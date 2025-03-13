from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime, timedelta
import os
import time

# Replace with your Alpha Vantage API key
API_KEY = 'OOCHOHZKJFOS5V35'

# File paths
CONSTITUENTS_FILE = 'index/sp500_constituents.csv'
OUTPUT_FILE = 'sp500_daily_data_alphavantage.csv'

# Read S&P 500 constituents
sp500_df = pd.read_csv(CONSTITUENTS_FILE)
symbols = sp500_df['Symbol'].tolist()  # Extract list of ticker symbols

# Initialize Alpha Vantage TimeSeries
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Check if output file exists and load existing dates per symbol to avoid duplicates
if os.path.exists(OUTPUT_FILE):
    existing_data = pd.read_csv(OUTPUT_FILE)
    existing_data['date'] = pd.to_datetime(existing_data['date'])
    existing_dates_by_symbol = {symbol: set(existing_data[existing_data['symbol'] == symbol]['date']) 
                                for symbol in existing_data['symbol'].unique()}
else:
    existing_dates_by_symbol = {}
    # Create an empty CSV with headers if it doesn't exist
    pd.DataFrame(columns=['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']).to_csv(OUTPUT_FILE, index=False)

# Get yesterday's date (latest complete trading day as of March 12, 2025)
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Fetch and append data for each symbol
for symbol in symbols:
    print(f"Fetching data for {symbol}...")
    try:
        # Get full daily data (earliest to latest)
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        
        # Rename columns
        data.columns = ['open', 'high', 'low', 'close', 'volume']
        data = data.reset_index()
        data['date'] = pd.to_datetime(data['date'])
        data['symbol'] = symbol
        
        # Filter out data already in the CSV (avoid duplicates)
        if symbol in existing_dates_by_symbol:
            data = data[~data['date'].isin(existing_dates_by_symbol[symbol])]
        
        # Append new data to CSV if there’s anything to add
        if not data.empty:
            # Append mode to avoid loading entire file into memory
            data[['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']].to_csv(
                OUTPUT_FILE, mode='a', header=False, index=False
            )
            print(f"Added {len(data)} new rows for {symbol}")
            
            # Update the in-memory set of dates for this symbol
            if symbol not in existing_dates_by_symbol:
                existing_dates_by_symbol[symbol] = set()
            existing_dates_by_symbol[symbol].update(data['date'])
        else:
            print(f"No new data for {symbol}")
            
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
    
    # Respect Alpha Vantage free tier limit (5 calls/minute)
    # time.sleep(12)  # Wait 12 seconds between calls

print(f"Data collection complete. All data saved to {OUTPUT_FILE}")