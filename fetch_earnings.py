import requests
import json
from datetime import datetime, timedelta

def fetch_tradingview_earnings():
    url = "https://scanner.tradingview.com/united-states/scan"
    headers = {"Content-Type": "application/json"}

    today = datetime.utcnow().date()
    start_day = today + timedelta(days=2)
    end_day = today + timedelta(days=10)

    payload = {
        "filter": [
            {"left": "earnings.earnings_release_date", "operation": "nempty"},
            {"left": "options.is_tradable", "operation": "equal", "right": True}
        ],
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": ["symbol", "description", "earnings.earnings_release_date"],
        "sort": {"sortBy": "earnings.earnings_release_date", "sortOrder": "asc"},
        "range": [0, 1000]
    }

    response = requests.post(url, headers=headers, json=payload)

    # 錯誤處理：TradingView 有時會返回 HTML（404）而非 JSON
    try:
        data = response.json()
    except Exception as e:
        print("❌ Not a JSON response:")
        print(response.text)
        raise Exception("Invalid response type")

    results = []
    for entry in data.get("data", []):
        try:
            symbol = entry["d"][0]
            name = entry["d"][1]
            date_str = entry["d"][2].split("T")[0]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            if start_day <= date_obj <= end_day:
                results.append({
                    "symbol": symbol,
                    "company": name,
                    "date": date_str
                })
        except Exception:
            continue

    with open("mock_upcoming_earnings.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Saved {len(results)} earnings entries to mock_upcoming_earnings.json")

if __name__ == "__main__":
    fetch_tradingview_earnings()
