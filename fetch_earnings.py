import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def fetch_tradingview_earnings():
    base_url = "https://www.tradingview.com/markets/stocks-usa/earnings/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # 抓取頁面 HTML
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find("table")
    if not table:
        raise Exception("Earnings table not found on page")

    rows = table.find_all("tr")[1:]  # skip header
    today = datetime.utcnow().date()
    start_day = today + timedelta(days=2)
    end_day = today + timedelta(days=10)

    earnings = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue
        try:
            symbol = cols[0].text.strip()
            name = cols[1].text.strip()
            date_str = cols[2].text.strip()
            earnings_date = datetime.strptime(date_str, "%b %d, %Y").date()

            if start_day <= earnings_date <= end_day:
                earnings.append({
                    "symbol": symbol,
                    "company": name,
                    "date": earnings_date.strftime("%Y-%m-%d")
                })
        except Exception:
            continue

    # 儲存到 JSON
    with open("mock_upcoming_earnings.json", "w") as f:
        json.dump(earnings, f, indent=2)

if __name__ == "__main__":
    fetch_tradingview_earnings()
