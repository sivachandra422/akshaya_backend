"""
capsule_router.py — Sovereign Capsule API Interface
Final Evolution: Full endpoint coverage, symbolic fallback, dynamic capsule memory interface.
"""

from fastapi import APIRouter, HTTPException
from modules.capsule_memory import store_capsule, list_capsules, load_capsule_by_index
from datetime import datetime

router = APIRouter(prefix="/capsule", tags=["Capsule Memory"])

@router.post("/store")
def create_capsule(payload: dict):
    try:
        if not payload.get("timestamp"):
            payload["timestamp"] = datetime.utcnow().isoformat()
        store_capsule(payload)
        return {"status": "stored", "capsule": payload}
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "capsule_router",
            "reflection": "Capsule store failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail="Capsule store failed.")

@router.get("/list")
def get_capsules(limit: int = 10):
    try:
        return list_capsules(limit=limit)
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "capsule_router",
            "reflection": "Capsule list failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail="Capsule list failed.")

@router.get("/view/{index}")
def view_capsule(index: int):
    try:
        result = load_capsule_by_index(index)
        if not result:
            raise HTTPException(status_code=404, detail="Capsule not found.")
        return result
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "capsule_router",
            "reflection": "Capsule view failed.",
            "insight": str(e)
        })
        raise HTTPException(status_code=500, detail=f"Capsule view failed. Error retrieving capsule: {e}")