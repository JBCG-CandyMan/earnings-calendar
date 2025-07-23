
import json
from datetime import datetime, timedelta

# Simulated earnings data
earnings = [
    {"symbol": "TSLA", "company": "Tesla Inc", "date": "2025-07-24", "time": "AMC", "eps": 0.83, "epsActual": None},
    {"symbol": "AAPL", "company": "Apple Inc", "date": "2025-07-25", "time": "BMO", "eps": 1.25, "epsActual": None}
]

# Save to JSON
with open("mock_upcoming_earnings.json", "w") as f:
    json.dump(earnings, f, indent=2)
