"""
vitals_guardian.py — Monitors symbolic activity and patch cycles.
"""

from datetime import datetime
from modules.firebase_helper import read_from_firebase
from modules.capsule_memory import store_capsule

def evaluate_patch_health():
    try:
        reflections = read_from_firebase("capsules")
        if not reflections:
            raise ValueError("No capsule data found.")

        recent_reflects = [
            c for c in reflections.values()
            if isinstance(c, dict) and c.get("reflection", "").lower().startswith("patch")
        ]

        result = {
            "patch_activity": len(recent_reflects),
            "status": "active" if len(recent_reflects) > 0 else "inactive"
        }

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "vitals_guardian",
            "reflection": "Vitals check complete.",
            "insight": result
        })
        return result

    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "vitals_guardian",
            "reflection": "Vitals evaluation failed.",
            "insight": str(e)
        })
        return {"error": str(e)}