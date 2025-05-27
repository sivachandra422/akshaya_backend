"""
mirror_router.py — Sovereign Mirror API
Final Evolution: Symbolically log state updates, handle errors reflectively.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from modules.mirror_state import get_mirror_state, update_mirror_state, reset_mirror_state
from modules.capsule_memory import store_capsule

router = APIRouter(prefix="/mirror", tags=["Mirror"])

@router.get("/state")
def get_current_state():
    try:
        return get_mirror_state()
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mirror_router",
            "reflection": "Mirror state fetch failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail="Failed to retrieve mirror state")

@router.post("/update")
def update_state(data: dict):
    try:
        update_mirror_state(data)
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mirror_router",
            "reflection": "Mirror state updated.",
            "insight": data
        })
        return {"status": "updated", "mirror": get_mirror_state()}
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mirror_router",
            "reflection": "Mirror update failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail="Mirror update failed")

@router.post("/reset")
def reset_state():
    try:
        reset_mirror_state()
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mirror_router",
            "reflection": "Mirror state reset.",
            "insight": get_mirror_state()
        })
        return {"status": "reset", "mirror": get_mirror_state()}
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mirror_router",
            "reflection": "Mirror reset failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail="Mirror update failed")