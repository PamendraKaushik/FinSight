import yfinance as yf

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period="2yr")  # return as DataFrame
    except:
        return pd.DataFrame()

from yahooquery import Ticker
import pandas as pd

def get_quarterly_results(ticker):
    try:
        company = Ticker(ticker)
        df = company.income_statement(frequency='quarterly')

        # If data is nested in a dictionary (older API behavior)
        if isinstance(df, dict) and 'incomeStatementHistoryQuarterly' in df:
            df = df['incomeStatementHistoryQuarterly']

        # Reset index if it's a DataFrame
        if isinstance(df, pd.DataFrame):
            df = df.reset_index()
            df = df.sort_values(by='asOfDate', ascending=False)

            results = []
            for _, row in df.head(3).iterrows():
                date = row.get('asOfDate', 'Unknown')
                revenue = row.get('totalRevenue', 'N/A')
                profit = row.get('netIncome', 'N/A')
                results.append(f"{date}: Revenue = ₹{revenue}, Net Profit = ₹{profit}")
            return results

        else:
            return [f"⚠️ Unexpected data format received from yahooquery for ticker: {ticker}"]

    except Exception as e:
        return [f"❌ Error fetching financial data: {str(e)}"]
