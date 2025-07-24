import requests
import json
from datetime import datetime, timedelta

def fetch_tradingview_earnings():
    url = "https://scanner.tradingview.com/united-states/scan"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"  # 👈 這行不能少
    }

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
        "range": [0, 2000]
    }

    response = requests.post(url, json=payload, headers=headers)

    # ✅ 檢查是否為 JSON 格式，否則顯示錯誤訊息
    if "application/json" not in response.headers.get("Content-Type", ""):
        print("❌ Not JSON Response:")
        print(response.text[:300])
        raise Exception("Invalid response type (not JSON)")

    try:
        data = response.json()
    except Exception as e:
        print("❌ JSON decode failed:", e)
        print(response.text[:300])
        raise

    result = []
    for d in data.get("data", []):
        try:
            symbol = d["d"][0]
            name = d["d"][1]
            date_str = d["d"][2].split("T")[0]
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_day <= date <= end_day:
                result.append({
                    "symbol": symbol,
                    "company": name,
                    "date": date_str
                })
        except Exception:
            continue

    with open("mock_upcoming_earnings.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Saved {len(result)} earnings items to mock_upcoming_earnings.json")

if __name__ == "__main__":
    fetch_tradingview_earnings()
