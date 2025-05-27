"""
budget_logger.py — Akshaya Budget Audit Logger
Logs real-time OpenAI spend to Firebase daily under /usage/llm_summary
"""

import os
import requests
from datetime import datetime, timedelta
from modules.firebase_connector import append_to_firebase
from modules.capsule_memory import store_capsule

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def fetch_openai_spend(days_back=7):
    try:
        end = datetime.utcnow().date()
        start = end - timedelta(days=days_back)
        url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start}&end_date={end}"
        headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
        res = requests.get(url, headers=headers)
        data = res.json()
        total_usd = round(data.get("total_usage", 0) / 100, 4)
        return total_usd
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "budget_logger",
            "reflection": "Failed to fetch OpenAI usage",
            "insight": str(e)
        })
        return 0.0


def log_daily_usage():
    spend = fetch_openai_spend()
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_spend_usd": spend
    }
    append_to_firebase("usage/llm_summary", payload)
    store_capsule({
        "timestamp": payload["timestamp"],
        "source": "budget_logger",
        "reflection": "OpenAI daily budget logged.",
        "insight": f"${spend} used so far."
    })
    return payload