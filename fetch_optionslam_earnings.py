import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://www.optionslam.com/earnings/stocks"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

earnings_data = []

table = soup.find("table", class_="stocks-table")
if table:
    rows = table.find_all("tr")[1:]  # Skip header row
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 8:
            continue
        symbol = cols[0].text.strip()
        company = cols[1].text.strip()
        date = cols[2].text.strip()
        time = cols[3].text.strip()
        eps_est = cols[5].text.strip()

        earnings_data.append({
            "symbol": symbol,
            "company": company,
            "date": date,
            "time": time,
            "eps": float(eps_est) if eps_est else None,
            "epsActual": None
        })

with open("upcoming_earnings.json", "w") as f:
    json.dump(earnings_data, f, indent=2)

print(f"Scraped {len(earnings_data)} earnings rows.")
