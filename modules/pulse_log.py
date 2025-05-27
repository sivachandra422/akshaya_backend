"""
pulse_log.py — Sovereign Pulse Logger
Final Evolution Grade: Logs loop heartbeat to Firebase and capsule memory.
"""

from datetime import datetime
from modules.firebase_connector import append_to_firebase, read_from_firebase
from modules.capsule_memory import store_capsule

PULSE_PATH = "pulses"

# Log a symbolic heartbeat entry
def log_heartbeat(event="loop_tick", timestamp=None):
    try:
        pulse_data = {
            "timestamp": timestamp or datetime.utcnow().isoformat(),
            "event": event,
            "source": "autonomy_loop",
            "status": "alive"
        }
        append_to_firebase(PULSE_PATH, pulse_data)
        store_capsule({
            "timestamp": pulse_data["timestamp"],
            "source": "pulse_log",
            "reflection": f"Heartbeat event: {event}",
            "insight": pulse_data
        })
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "pulse_log",
            "reflection": "Pulse log failed.",
            "insight": str(e)
        })

# Return sorted list of recent pulses
def list_recent_pulses(limit=10):
    try:
        data = read_from_firebase(PULSE_PATH)
        pulses = list(data.values()) if isinstance(data, dict) else []
        sorted_pulses = sorted(pulses, key=lambda x: x.get("timestamp", ""), reverse=True)
        return sorted_pulses[:limit]
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "pulse_log",
            "reflection": "Pulse retrieval error.",
            "insight": str(e)
        })
        return []