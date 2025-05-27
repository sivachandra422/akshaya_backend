"""
usage_router.py — Token & Cost Monitoring Interface
Final Evolution: Sovereign route exposing real-time token usage, cost trends, and fallback status.
"""

from fastapi import APIRouter, HTTPException
from modules.firebase_connector import read_from_firebase
from datetime import datetime

router = APIRouter(prefix="/usage", tags=["Usage Monitor"])

@router.get("/status")
def get_llm_usage():
    try:
        data = read_from_firebase("usage/llm")
        if not data:
            return {"status": "ok", "message": "No LLM usage data yet."}

        summary = {}
        total_cost = 0.0
        for _, entry in data.items():
            model = entry.get("model")
            cost = float(entry.get("cost", 0))
            summary[model] = summary.get(model, 0.0) + cost
            total_cost += cost

        return {
            "status": "ok",
            "total_spent_usd": round(total_cost, 4),
            "per_model": {k: round(v, 4) for k, v in summary.items()},
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to retrieve usage data.",
            "insight": str(e)
        }