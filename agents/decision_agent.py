from core.ollama_wrapper import run_llm
from tools.stock_fetcher import get_quarterly_results  # Make sure you have this
import pandas as pd

def calculate_pct_change(close_prices: dict):
    try:
        prices = list(close_prices.values())
        if len(prices) >= 2:
            return round((prices[-1] - prices[0]) / prices[0] * 100, 2)
    except:
        return None
    return None

def generate_answer(query, news, sentiments, stock_data, doc_text, model, temperature, ticker=None):
    facts = []

    # 1. Stock price trend
    if stock_data and isinstance(stock_data, dict) and "Close" in stock_data:
        pct_change = calculate_pct_change(stock_data["Close"])
        if pct_change is not None:
            facts.append(f"📈 Stock price changed by {pct_change}% over the last 3 months.")

    # 2. Sentiment summary
    if sentiments:
        pos = sum(1 for s in sentiments if s["sentiment"] == "Positive")
        neg = sum(1 for s in sentiments if s["sentiment"] == "Negative")
        neu = sum(1 for s in sentiments if s["sentiment"] == "Neutral")
        facts.append(f"🗞️ News sentiment: {pos} positive, {neg} negative, and {neu} neutral headlines.")

    # 3. Latest financials
    if ticker:
        financials = get_quarterly_results(ticker)
        if financials:
            facts.append("📊 Last 3 quarterly results:")
            facts.extend([f"- {item}" for item in financials[:3]])

    # 4. Document snippet
    if doc_text:
        snippet = doc_text[:300].replace("\n", " ")
        facts.append(f"📄 Extracted document snippet: {snippet}...")

    # 5. Fallback if no facts found
    if not facts:
        return "❌ I couldn't find any relevant financial data to answer that. Please refine your question or upload a report."

    # 6. Build final prompt
    fact_block = "\n".join(facts)
    prompt = f"""
You are a professional financial advisor.

Use the following factual data to answer the user's question. Do not make up any numbers. If data is missing, acknowledge it.

💬 Question: {query}

📚 Facts:
{fact_block}

🧠 Answer:
"""

    # 7. Run the model
    response = run_llm(model, prompt, temperature=temperature)
    return response
