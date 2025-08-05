def plan_actions(query: str):
    query_lower = query.lower()
    actions = {
        "use_doc_agent": "report" in query_lower or "pdf" in query_lower,
        "use_news_agent": "news" in query_lower or "market" in query_lower or "sentiment" in query_lower,
        "use_trend_agent": "trend" in query_lower or "stock" in query_lower or "price" in query_lower,
    }
    return actions
