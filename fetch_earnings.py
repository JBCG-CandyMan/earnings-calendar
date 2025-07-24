import requests

url = "https://scanner.tradingview.com/united-states/scan"
headers = {"Content-Type": "application/json"}

payload = {
    "filter": [
        {"left": "earnings.earnings_release_date", "operation": "nempty"},
        {"left": "options.is_tradable", "operation": "equal", "right": True}
    ],
    "symbols": {"query": {"types": []}, "tickers": []},
    "columns": ["symbol", "description", "earnings.earnings_release_date"],
    "sort": {"sortBy": "earnings.earnings_release_date", "sortOrder": "asc"},
    "range": [0, 5]
}

resp = requests.post(url, headers=headers, json=payload)

print("HTTP Status Code:", resp.status_code)
print("Response preview:", resp.text[:500])
