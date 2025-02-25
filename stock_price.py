# stock_price.py
import yfinance as yf
from datetime import datetime, timedelta

def get_stock_prices(tickers, date):
    """
    Fetch stock prices for given tickers on a specific date.
    
    Args:
        tickers (list): List of stock ticker symbols (e.g., ['AAPL', 'TSLA']).
        date (datetime): Date for which to fetch prices.
    
    Returns:
        dict: Mapping of tickers to their closing prices.
    """
    prices = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=date, end=date + timedelta(days=1))
        if not hist.empty:
            prices[ticker] = hist["Close"].iloc[-1]
        else:
            prices[ticker] = None  # Handle missing data
    return prices

# Test function (optional, for standalone testing)
if __name__ == "__main__":
    sample_date = datetime.strptime("2025-02-24", "%Y-%m-%d")
    sample_tickers = ["AAPL", "TSLA"]
    prices = get_stock_prices(sample_tickers, sample_date)
    print(f"Stock Prices: {prices}")