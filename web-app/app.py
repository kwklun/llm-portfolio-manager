# app.py
import os
import pickle
import numpy as np
from flask import Flask, request, render_template, jsonify
from statsmodels.tsa.arima.model import ARIMA
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

app = Flask(__name__)

# Define the path to the ARIMA models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of app.py
MODEL_FOLDER = os.path.join(BASE_DIR, "../model_training/model_trained/arima")  # Adjust path to models
WATCHLIST_FILE = os.path.join(BASE_DIR, "watchlist.csv")  # Absolute path to watchlist.csv

# Eastern Time Zone for U.S. market hours
ET = pytz.timezone('US/Eastern')

def is_market_open():
    """Check if the U.S. market is open (9:30 AM to 4:00 PM Eastern, Mon-Fri)."""
    now = datetime.now(ET)
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    # Check if it's a weekday (Monday=0, Sunday=6)
    is_weekday = now.weekday() < 5
    # Check if current time is within market hours
    is_within_hours = market_open.time() <= now.time() <= market_close.time()
    return is_weekday and is_within_hours

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_price = None
    error_message = None
    ticker = None
    watchlist = []
    watchlist_data = []

    # Load watchlist from CSV
    try:
        watchlist_df = pd.read_csv(WATCHLIST_FILE)
        watchlist = watchlist_df['Symbol'].str.upper().tolist()
        print(watchlist_df)
    except FileNotFoundError:
        error_message = f"Watchlist file '{WATCHLIST_FILE}' not found."
    except KeyError:
        error_message = f"Watchlist CSV must have a 'Symbol' column."

    # Fetch initial prices for watchlist
    if watchlist:
        try:
            for symbol in watchlist:
                stock = yf.Ticker(symbol)
                price = stock.info.get('regularMarketPrice', stock.info.get('regularMarketPreviousClose', 'N/A'))
                if price == 'N/A':
                    price = 'N/A'
                else:
                    price = round(price, 2)
                watchlist_data.append({'symbol': symbol, 'price': price})
        except Exception as e:
            error_message = f"Error fetching watchlist prices: {str(e)}"

    # Determine market status
    market_status = "Open" if is_market_open() else "Closed"

    # Handle prediction form submission
    if request.method == 'POST':
        ticker = request.form.get('ticker', '').strip().upper()
        if not ticker:
            error_message = "Please enter a ticker symbol."
        else:
            try:
                # Load the model for the given ticker
                model_file = os.path.join(MODEL_FOLDER, f'arima_model_{ticker}_pre_20250312.pkl')
                if not os.path.exists(model_file):
                    error_message = f"No model found for ticker '{ticker}'."
                else:
                    with open(model_file, 'rb') as f:
                        model_data = pickle.load(f)

                    # Extract model components
                    params = model_data['params']
                    order = model_data['order']
                    last_p_obs = model_data['last_p_obs']

                    # Log for debugging
                    print(f"Ticker: {ticker}")
                    print(f"Order: {order}")
                    print(f"Last p observations: {last_p_obs}")
                    print(f"Parameters: {params}")

                    # Reconstruct the ARIMA model
                    model = ARIMA(last_p_obs, order=order)
                    model_fit = model.fit(start_params=params)

                    # Forecast the next stock price (1 step ahead)
                    forecast = model_fit.forecast(steps=1)
                    if isinstance(forecast, np.ndarray):
                        predicted_value = forecast[0]  # Use array indexing for numpy.ndarray
                    else:
                        predicted_value = forecast.iloc[0]  # Fallback for Pandas Series

                    # Check for valid prediction
                    if np.isnan(predicted_value) or np.isinf(predicted_value):
                        raise ValueError("Prediction resulted in invalid value (NaN or Inf).")
                    
                    predicted_price = round(predicted_value, 2)

            except Exception as e:
                error_message = f"Error predicting price for {ticker}: {str(e)}"

    return render_template(
        'index.html',
        predicted_price=predicted_price,
        error_message=error_message,
        ticker=ticker,
        watchlist_data=watchlist_data,
        market_status=market_status
    )

@app.route('/update_prices', methods=['GET'])
def update_prices():
    """API endpoint to fetch updated prices for the watchlist."""
    try:
        watchlist_df = pd.read_csv(WATCHLIST_FILE)
        watchlist = watchlist_df['Symbol'].str.upper().tolist()
        updated_prices = []
        for symbol in watchlist:
            stock = yf.Ticker(symbol)
            price = stock.info.get('regularMarketPrice', stock.info.get('regularMarketPreviousClose', 'N/A'))
            if price == 'N/A':
                price = 'N/A'
            else:
                price = round(price, 2)
            updated_prices.append({'symbol': symbol, 'price': price})
        return jsonify(updated_prices)
    except Exception as e:
        return jsonify({'error': f"Error fetching prices: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)