# fetch_earnings.py
import requests
import json
from datetime import datetime, timedelta

def fetch_tradingview_earnings(days_ahead=10):
    url = 'https://scanner.tradingview.com/united-states/scan'
    headers = {'Content-Type': 'application/json'}
    today = datetime.utcnow()
    future = today + timedelta(days=days_ahead)

    payload = {
        "symbols": {
            "tickers": [],
            "query": {"types": []}
        },
        "columns": [
            "logoid", "name", "earnings_release_date", "market_cap_basic", "optionable"
        ],
        "filter": [
            {"left": "earnings_release_date", "operation": "nempty"},
            {"left": "earnings_release_date", "operation": "greater", "right": int(today.timestamp())},
            {"left": "earnings_release_date", "operation": "less", "right": int(future.timestamp())},
            {"left": "optionable", "operation": "equal", "right": True}
        ],
        "sort": {"sortBy": "earnings_release_date", "sortOrder": "asc"},
        "options": {"lang": "en"}
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise Exception("Failed to fetch data from TradingView")

    results = response.json().get("data", [])
    earnings = []
    for r in results:
        d = r["d"]
        ticker = d[1]
        earnings_date = datetime.utcfromtimestamp(d[2]).strftime("%Y-%m-%d")
        earnings.append({"symbol": ticker, "date": earnings_date})

    return earnings

if __name__ == "__main__":
    earnings = fetch_tradingview_earnings()
    with open("mock_upcoming_earnings.json", "w") as f:
        json.dump(earnings, f, indent=2)
