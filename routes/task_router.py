"""
task_router.py — Sovereign Task Engine Interface
Final Evolution: Capsule-backed heartbeat, patch cycle trigger, and symbolic note logging.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from services.reflection_trigger import auto_reflect_and_patch
from modules.pulse_log import log_heartbeat
from modules.capsule_memory import store_capsule

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/heartbeat")
def manual_heartbeat():
    now = datetime.utcnow().isoformat()
    try:
        log_heartbeat(event="manual")
        store_capsule({
            "timestamp": now,
            "source": "task_router",
            "reflection": "Manual heartbeat invoked.",
            "insight": "Triggered via API."
        })
        return {"status": "heartbeat-logged", "timestamp": now}
    except Exception as e:
        store_capsule({
            "timestamp": now,
            "source": "task_router",
            "reflection": "Manual heartbeat failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail="Heartbeat failed")

@router.post("/patch")
def task_trigger_patch():
    now = datetime.utcnow().isoformat()
    try:
        auto_reflect_and_patch(now)
        store_capsule({
            "timestamp": now,
            "source": "task_router",
            "reflection": "Scheduled patch cycle triggered.",
            "insight": "Called from /patch endpoint."
        })
        return {"status": "patch-cycle-triggered", "timestamp": now}
    except Exception as e:
        store_capsule({
            "timestamp": now,
            "source": "task_router",
            "reflection": "Patch trigger failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail="Patch trigger failed")

@router.post("/note")
def log_custom_task_note(data: dict):
    timestamp = datetime.utcnow().isoformat()
    try:
        note = {
            "timestamp": timestamp,
            "source": "task_router",
            "reflection": data.get("reflection", "Manual note triggered by API."),
            "insight": data.get("insight", "No specific insight provided.")
        }
        store_capsule(note)
        return {"status": "note-logged", "timestamp": timestamp}
    except Exception as e:
        store_capsule({
            "timestamp": timestamp,
            "source": "task_router",
            "reflection": "Note logging failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail="Note log failed")