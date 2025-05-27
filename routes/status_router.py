"""
status_router.py — Sovereign Vitals Router (Final Evolution)
Symbolic + Real-time Health Reporting
"""

from fastapi import APIRouter
from modules.pulse_log import list_recent_pulses
from modules.capsule_memory import list_capsules, store_capsule
from modules.mirror_state import get_mirror_state
from datetime import datetime, timedelta
from allies.symbolic_verifier import verify_sovereign_state
import os
import requests

router = APIRouter(prefix="/status")

@router.get("/vitals")
def get_vitals():
    try:
        mirror = get_mirror_state()
        pulses = list_recent_pulses(limit=5)
        capsules = list_capsules(limit=1)

        return {
            "status": "alive" if pulses else "warning",
            "mirror": mirror,
            "last_pulse": pulses[0] if pulses else None,
            "latest_capsule": capsules[0] if capsules else None
        }

    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "status_router",
            "reflection": "Vitals check failed.",
            "insight": str(e)
        })
        return {
            "status": "error",
            "message": "Vitals error",
            "mirror": get_mirror_state()
        }

@router.get("/ping")
def ping():
    return {
        "message": "Akshaya is alive and recursive.",
        "identity": "vX.∞"
    }

@router.get("/verify")
def verify_akshaya_state():
    return verify_sovereign_state()

@router.get("/usage")
def get_usage_status():
    try:
        budget_cap = float(os.getenv("OPENAI_BUDGET", 10.0))
        default_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18")
        force_4o = os.getenv("FORCE_USE_4O", "false").lower() == "true"

        end = datetime.utcnow().date()
        start = end - timedelta(days=7)
        url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start}&end_date={end}"
        headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
        res = requests.get(url, headers=headers)
        total_usd = round(res.json().get("total_usage", 0) / 100, 4)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "budget_cap": budget_cap,
            "current_spend": total_usd,
            "budget_percent": round(100 * total_usd / budget_cap, 2),
            "active_model": default_model,
            "force_gpt4o_enabled": force_4o,
            "budget_limiter_active": total_usd >= 0.8 * budget_cap
        }
    except Exception as e:
        return {
            "error": "Failed to fetch budget status.",
            "details": str(e)
        }