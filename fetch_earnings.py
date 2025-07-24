import requests
import json
from datetime import datetime, timedelta

def fetch_tradingview_earnings():
    url = "https://scanner.tradingview.com/united-states/scan"
    headers = {"content-type": "application/json"}

    today = datetime.utcnow().date()
    start_day = today + timedelta(days=2)
    end_day = today + timedelta(days=10)

    payload = {
        "filter": [
            {"left": "earnings.earnings_release_date", "operation": "nempty"},
            {"left": "options.is_tradable", "operation": "equal", "right": True}
        ],
        "symbols": {"tickers": [], "query": {"types": []}},
        "columns": ["symbol", "description", "earnings.earnings_release_date"],
        "sort": {"sortBy": "earnings.earnings_release_date", "sortOrder": "asc"},
        "range": [0, 2000]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        if "application/json" not in response.headers.get("Content-Type", ""):
            raise Exception("Invalid response type: not JSON")

        data = response.json()

        results = []
        for row in data.get("data", []):
            symbol, company, date_str = row["d"]
            date_only = date_str.split("T")[0]
            date_obj = datetime.strptime(date_only, "%Y-%m-%d").date()
            if start_day <= date_obj <= end_day:
                results.append({
                    "symbol": symbol,
                    "company": company,
                    "date": date_only
                })

        with open("mock_upcoming_earnings.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"✅ Saved {len(results)} earnings to mock_upcoming_earnings.json")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    fetch_tradingview_earnings()
