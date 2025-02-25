# main.py
from datetime import datetime
import pandas as pd
from ast import literal_eval
import argparse
from stock_price import get_stock_prices  # API call for stock prices
from financial_news import get_news      # API call for news
from llm_advice import get_investment_advice

SAMPLE_DATA_DIR = "sample_data"

def load_portfolio(file_path=f"{SAMPLE_DATA_DIR}/portfolio.csv"):
    """Load portfolio from CSV."""
    df = pd.read_csv(file_path)
    portfolio = {
        "cash": float(df["cash"].iloc[0]),
        "stocks": literal_eval(df["stocks"].iloc[0]),
        "risk_level": df["risk_level"].iloc[0]
    }
    return portfolio

def load_stock_prices(file_path=f"{SAMPLE_DATA_DIR}/stock_prices.csv", date_str="2025-02-24"):
    """Load stock prices from CSV for a specific date."""
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    date = datetime.strptime(date_str, "%Y-%m-%d")
    prices_df = df[df["date"] == date]
    return dict(zip(prices_df["ticker"], prices_df["price"]))

def load_news(file_path=f"{SAMPLE_DATA_DIR}/news.csv", date_str="2025-02-24"):
    """Load news from CSV for a specific date."""
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    date = datetime.strptime(date_str, "%Y-%m-%d")
    news_row = df[df["date"] == date]
    return news_row["news"].iloc[0] if not news_row.empty else "No news available."

def get_data(portfolio_source="file", stock_prices_source="file", news_source="file", date_str="2025-02-24"):
    """Fetch or load data based on source selection."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Portfolio
    if portfolio_source.lower() == "file":
        portfolio = load_portfolio()
    else:  # API (placeholder, no portfolio API provided)
        portfolio = {"cash": 5000, "stocks": {"AAPL": 10, "TSLA": 5}, "risk_level": "Moderate"}
        print("Warning: Portfolio API not implemented, using default portfolio.")
    
    # Stock Prices
    tickers = list(portfolio["stocks"].keys())
    if stock_prices_source.lower() == "file":
        stock_prices = load_stock_prices(date_str=date_str)
    else:  # API
        stock_prices = get_stock_prices(tickers, date)  # Using your API call
    
    # News
    if news_source.lower() == "file":
        news = load_news(date_str=date_str)
    else:  # API
        news = get_news(date, tickers)  # Using your API call
    
    return portfolio, stock_prices, news

def main(portfolio_source="file", stock_prices_source="file", news_source="file"):
    date_str = "2025-02-24"  # Fixed date for this example
    
    # Get data based on source preferences
    portfolio, stock_prices, news = get_data(portfolio_source, stock_prices_source, news_source, date_str)
    
    # Get investment advice from Grok 3
    advice = get_investment_advice("grok3", portfolio, stock_prices, news)
    
    # Output results
    print(f"Date: {date_str}")
    print(f"Portfolio: {portfolio}")
    print(f"Stock Prices: {stock_prices}")
    print(f"News:\n{news}")
    print(f"Grok 3 Investment Advice:\n{advice}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LLM portfolio manager with data source options.")
    parser.add_argument("--portfolio", choices=["file", "api"], default="file", help="Source for portfolio data")
    parser.add_argument("--stock-prices", choices=["file", "api"], default="file", help="Source for stock prices")
    parser.add_argument("--news", choices=["file", "api"], default="file", help="Source for news")
    args = parser.parse_args()
    
    main(args.portfolio, args.stock_prices, args.news)