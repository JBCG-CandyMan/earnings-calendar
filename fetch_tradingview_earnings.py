import requests
import json
from datetime import datetime, timedelta

def fetch_tradingview_earnings():
    today = datetime.today()
    from_date = today + timedelta(days=1)
    to_date = today + timedelta(days=10)

    url = "https://scanner.tradingview.com/america/scan"
    payload = {
        "filter": [
            {
                "left": "earnings.earnings_release_date",
                "operation": "between",
                "right": [from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d")]
            },
            {
                "left": "optionable",
                "operation": "equal",
                "right": True
            }
        ],
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": [
            "name",
            "description",
            "earnings.earnings_release_date",
            "earnings.earnings_release_time",
            "earnings.per_share_estimate",
            "earnings.per_share_actual"
        ],
        "sort": {
            "sortBy": "earnings.earnings_release_date",
            "sortOrder": "asc"
        },
        "options": {"lang": "en"}
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    results = []
    for item in data.get("data", []):
        d = item["d"]
        result = {
            "symbol": d[0],
            "company": d[1],
            "date": d[2],
            "time": d[3],
            "eps": d[4],
            "epsActual": d[5]
        }
        results.append(result)

    with open("mock_upcoming_earnings.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    fetch_tradingview_earnings()
