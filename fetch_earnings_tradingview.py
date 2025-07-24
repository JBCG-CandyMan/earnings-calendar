import requests
import json
from datetime import datetime, timedelta

def fetch_tradingview_earnings():
    url = "https://scanner.tradingview.com/united-states/scan"
    headers = {"content-type": "application/json"}
    
    today = datetime.utcnow().date()
    end_day = today + timedelta(days=10)
    start_day = today + timedelta(days=2)

    payload = {
        "filter": [
            {"left": "earnings.earnings_release_date", "operation": "nempty"},
            {"left": "options.is_tradable", "operation": "equal", "right": True}
        ],
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": ["symbol", "description", "earnings.earnings_release_date"],
        "sort": {"sortBy": "earnings.earnings_release_date", "sortOrder": "asc"},
        "range": [0, 2000]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    result = []
    for d in data["data"]:
        try:
            sym = d["d"][0]
            name = d["d"][1]
            date_str = d["d"][2].split("T")[0]
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_day <= date <= end_day:
                result.append({
                    "symbol": sym,
                    "company": name,
                    "date": date_str
                })
        except Exception:
            continue

    with open("mock_upcoming_earnings.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    fetch_tradingview_earnings()
