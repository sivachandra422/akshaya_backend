"""
mode_ally.py — Runtime Mode Enforcement Ally
Final Evolution: Ensures system honors active mode logic. Enables sovereign task skipping and symbolic trace.
"""

from modules.firebase_helper import read_from_firebase
from modules.capsule_memory import store_capsule
from datetime import datetime

MODE_PATH = "mirror/mode"
DEFAULT_MODE = "active"

# Get current runtime mode
def get_current_mode():
    try:
        mode = read_from_firebase(MODE_PATH)
        return mode if mode else DEFAULT_MODE
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mode_ally",
            "reflection": "Mode fetch failed. Using fallback.",
            "insight": str(e)
        })
        return DEFAULT_MODE

# Decide if a task should run
def should_run(task_type: str):
    mode = get_current_mode()
    logic = {
        "active": True,
        "low_power": task_type in ["heartbeat", "note"],
        "reflection_only": task_type in ["note", "reflect"]
    }
    decision = logic.get(mode, True)

    if not decision:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mode_ally",
            "reflection": f"Task blocked in {mode} mode.",
            "insight": {"task_type": task_type}
        })

    return decision