# financial_news.py
from datetime import datetime
from newsapi import NewsApiClient
from config import NEWSAPI_KEY  # Import key from config

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

def get_news(date, tickers):
    query = " OR ".join(tickers) + " finance stock market"
    date_str = date.strftime("%Y-%m-%d")
    articles = newsapi.get_everything(
        q=query,
        from_param=date_str,
        to=date_str,
        language="en",
        sort_by="relevancy",
        page_size=3
    )
    if articles["status"] == "ok" and articles["totalResults"] > 0:
        news_summary = f"Financial News for {date_str}:\n"
        for article in articles["articles"]:
            news_summary += f"- {article['title']} ({article['source']['name']})\n"
        return news_summary.strip()
    else:
        return f"No news found for {date_str}."

if __name__ == "__main__":
    sample_date = datetime.strptime("2025-02-24", "%Y-%m-%d")
    sample_tickers = ["AAPL", "TSLA"]
    news = get_news(sample_date, sample_tickers)
    print(news)