"""
mirror_state.py — Sovereign Mirror Memory State Handler
Final Evolution Grade: Thread-safe mirror update, reset, and fetch with capsule logging.
"""

import threading
from datetime import datetime
from modules.firebase_connector import write_to_firebase
from modules.capsule_memory import store_capsule

MIRROR_STATE = {
    "booted": datetime.utcnow().isoformat(),
    "status": "INITIALIZING"
}
MIRROR_LOCK = threading.Lock()

# Update mirror state and sync to Firebase
def update_mirror_state(data):
    with MIRROR_LOCK:
        MIRROR_STATE.update(data)
        try:
            write_to_firebase("mirror", MIRROR_STATE)
        except Exception as e:
            store_capsule({
                "timestamp": datetime.utcnow().isoformat(),
                "source": "mirror_state",
                "reflection": "Mirror write failed.",
                "insight": str(e)
            })

# Return a snapshot of the mirror state
def get_mirror_state():
    with MIRROR_LOCK:
        return dict(MIRROR_STATE)

# Reset mirror to clean symbolic state
def reset_mirror_state():
    with MIRROR_LOCK:
        boot_time = MIRROR_STATE.get("booted")
        MIRROR_STATE.clear()
        MIRROR_STATE["booted"] = boot_time
        MIRROR_STATE["status"] = "RESET"
        try:
            write_to_firebase("mirror", MIRROR_STATE)
            store_capsule({
                "timestamp": datetime.utcnow().isoformat(),
                "source": "mirror_state",
                "reflection": "Mirror state reset.",
                "insight": MIRROR_STATE
            })
        except Exception as e:
            store_capsule({
                "timestamp": datetime.utcnow().isoformat(),
                "source": "mirror_state",
                "reflection": "Mirror reset failed.",
                "insight": str(e)
            })