"""
vitals_guardian.py — Recursive Health Monitor & Pulse Integrity Ally
Final Evolution: Detects heartbeat gaps, capsule loss, reflection silence, and triggers symbolic alerts.
"""

from datetime import datetime, timedelta
from modules.firebase_helper import read_from_firebase
from modules.capsule_memory import store_capsule

HEARTBEAT_PATH = "pulse/heartbeat"
REFLECTION_PATH = "capsules"

# Core health validator
def evaluate_system_vitals():
    now = datetime.utcnow()
    try:
        # --- Heartbeat Check ---
        heartbeats = read_from_firebase(HEARTBEAT_PATH)
        latest_hb = max(heartbeats.values(), key=lambda x: x.get("timestamp", "")) if heartbeats else {}

        last_hb_time = datetime.fromisoformat(latest_hb.get("timestamp", "1900-01-01"))
        heartbeat_ok = (now - last_hb_time) < timedelta(minutes=5)

        # --- Reflection Activity Check ---
        reflections = read_from_firebase(REFLECTION_PATH)
        recent_reflects = [c for c in reflections.values() if c.get("reflection", "").lower().startswith("patch")]
        recent_ok = any(datetime.fromisoformat(c.get("timestamp", "1900-01-01")) > now - timedelta(hours=1) for c in recent_reflects)

        # --- Trigger capsule if abnormal ---
        if not heartbeat_ok or not recent_ok:
            store_capsule({
                "timestamp": now.isoformat(),
                "source": "vitals_guardian",
                "reflection": "System vitals degraded.",
                "insight": {
                    "heartbeat": "OK" if heartbeat_ok else "Missing",
                    "recent_reflection": "OK" if recent_ok else "Silent"
                }
            })

        return {
            "status": "ok" if heartbeat_ok and recent_ok else "degraded",
            "heartbeat": heartbeat_ok,
            "reflection": recent_ok,
            "last_heartbeat": latest_hb.get("timestamp", None)
        }

    except Exception as e:
        store_capsule({
            "timestamp": now.isoformat(),
            "source": "vitals_guardian",
            "reflection": "Vitals evaluation failed.",
            "insight": str(e)
        })
        return {"status": "error", "message": str(e)}