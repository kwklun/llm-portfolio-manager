# main.py
from datetime import datetime
from stock_price import get_stock_prices
from financial_news import get_news
from llm_advice import get_investment_advice

portfolio = {
    "cash": 5000,
    "stocks": {
        "AAPL": 10,
        "TSLA": 5
    },
    "risk_level": "Moderate"
}

def main():
    date_str = "2025-02-24"  # Using Feb 24 as Feb 25 data isn’t fully available yet
    date = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Fetch stock prices
    tickers = list(portfolio["stocks"].keys())
    stock_prices = get_stock_prices(tickers, date)
    
    # Fetch real financial news
    news = get_news(date, tickers)
    
    # Get investment advice from Grok 3
    advice = get_investment_advice("grok3", portfolio, stock_prices, news)
    
    # Output results
    print(f"Date: {date_str}")
    print(f"Portfolio: {portfolio}")
    print(f"Stock Prices: {stock_prices}")
    print(f"News:\n{news}")
    print(f"Grok 3 Investment Advice:\n{advice}")

if __name__ == "__main__":
    main()