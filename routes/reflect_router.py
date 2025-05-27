"""
reflect_router.py — Sovereign Self-Evolution API
Final Evolution: Triggers recursive patch cycles with symbolic trace.
"""

from fastapi import APIRouter
from datetime import datetime
from services.reflection_trigger import auto_reflect_and_patch
from modules.capsule_memory import store_capsule

router = APIRouter(prefix="/reflect", tags=["Reflection"])

@router.post("/trigger")
def trigger_reflection():
    timestamp = datetime.utcnow().isoformat()
    try:
        auto_reflect_and_patch(timestamp)
        store_capsule({
            "timestamp": timestamp,
            "source": "reflect_router",
            "reflection": "Manual reflection triggered.",
            "insight": "Patch and deploy initiated."
        })
        return {"status": "triggered", "timestamp": timestamp}
    except Exception as e:
        store_capsule({
            "timestamp": timestamp,
            "source": "reflect_router",
            "reflection": "Manual reflection trigger failed.",
            "insight": str(e)
        })
        return {"status": "error", "message": str(e)}

@router.get("/status")
def check_reflection_status():
    return {
        "status": "ready",
        "mirror": "Active",
        "symbolic": "Recursion pathway is intact."
    }