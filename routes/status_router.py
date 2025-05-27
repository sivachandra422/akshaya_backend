"""
status_router.py — Sovereign Vitals Router (Final Evolution)
Symbolic + Real-time Health Reporting
"""

from fastapi import APIRouter
from modules.pulse_log import list_recent_pulses
from modules.capsule_memory import list_capsules, store_capsule
from modules.mirror_state import get_mirror_state
from datetime import datetime
from allies.symbolic_verifier import verify_sovereign_state

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