"""
budget_ally.py — Sovereign Budget Monitor and Alert Ally
Final Evolution: Tracks OpenAI API spend, triggers capsule alerts, and changes system mode adaptively.
"""

from datetime import datetime
from modules.firebase_helper import read_from_firebase, write_to_firebase
from modules.capsule_memory import store_capsule

BUDGET_LIMIT = float(os.getenv("OPENAI_BUDGET", 10.0))
SYSTEM_MODE_PATH = "mirror/mode"

# Check if total usage exceeds budget
def evaluate_budget_threshold():
    try:
        data = read_from_firebase("usage/llm")
        if not data:
            return {"status": "ok", "message": "No usage data."}

        total_cost = sum(float(entry.get("cost", 0)) for entry in data.values())

        if total_cost >= BUDGET_LIMIT:
            # Switch mode to low_power
            write_to_firebase(SYSTEM_MODE_PATH, "low_power")
            store_capsule({
                "timestamp": datetime.utcnow().isoformat(),
                "source": "budget_ally",
                "reflection": "Budget exceeded. Switching to low_power mode.",
                "insight": {
                    "total_spent": total_cost,
                    "budget_limit": BUDGET_LIMIT
                }
            })
            return {"status": "warning", "mode": "low_power", "used": total_cost, "limit": BUDGET_LIMIT}

        return {"status": "ok", "mode": "active", "used": total_cost, "limit": BUDGET_LIMIT}

    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "budget_ally",
            "reflection": "Budget evaluation failed.",
            "insight": str(e)
        })
        return {"status": "error", "message": str(e)}