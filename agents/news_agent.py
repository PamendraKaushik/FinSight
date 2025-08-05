from tools.news_scraper import fetch_news
from tools.sentiment import analyze_sentiment

def analyze_news(company):
    articles = fetch_news(company)
    sentiments = [{"text": a, "sentiment": analyze_sentiment(a)} for a in articles]
    return articles, sentiments