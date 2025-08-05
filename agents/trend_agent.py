from tools.stock_fetcher import fetch_stock_data

def get_trend(ticker):
    return fetch_stock_data(ticker)