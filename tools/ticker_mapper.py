from yahooquery import search

def get_ticker(company_name):
    try:
        result = search(company_name)
        quotes = result.get("quotes", [])
        for item in quotes:
            if company_name.lower() == item.get("shortname", "").lower():
                return item["symbol"]
        for item in quotes:
            if company_name.lower() in item.get("shortname", "").lower():
                return item["symbol"]
        if quotes:
            return quotes[0]["symbol"]
    except Exception as e:
        print(f"Ticker lookup failed for {company_name}: {e}")
    return None
