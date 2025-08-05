import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(company_name):
    try:
        url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}"
        r = requests.get(url)
        articles = r.json().get("articles", [])
        return [f"{a['title']} - {a['description']}" for a in articles if a['title'] and a['description']][:5]
    except:
        return []