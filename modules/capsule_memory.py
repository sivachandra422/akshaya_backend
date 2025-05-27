"""
capsule_memory.py — Sovereign Capsule Store and Reflective Recall Engine
Final Evolution Grade: Validated writes, capsule schema checks, and reflection-safe reads.
"""

import os
import json
from datetime import datetime
from modules.firebase_connector import append_to_firebase, read_from_firebase

CAPSULE_DIR = os.getenv("CAPSULE_DIR", "capsules")
os.makedirs(CAPSULE_DIR, exist_ok=True)

# Schema keys expected in every capsule
REQUIRED_KEYS = ["timestamp", "source", "reflection"]

# Ensure capsule matches schema
def is_valid_capsule(data):
    return isinstance(data, dict) and all(key in data for key in REQUIRED_KEYS)

# Write capsule to both Firebase and local mirror
def store_capsule(data: dict):
    try:
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow().isoformat()

        if not is_valid_capsule(data):
            raise ValueError("Invalid capsule schema")

        append_to_firebase("capsules", data)

        date_str = data["timestamp"].split("T")[0]
        file_path = os.path.join(CAPSULE_DIR, f"capsule_{date_str}.json")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                entries = json.load(f)
        else:
            entries = []

        entries.append(data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)

    except Exception as e:
        fallback = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": "capsule_memory",
            "reflection": "Capsule write failed.",
            "insight": str(e)
        }
        try:
            append_to_firebase("capsules", fallback)
        except:
            pass

# Fetch latest capsules from Firebase, sorted by timestamp
def list_capsules(limit=10):
    try:
        data = read_from_firebase("capsules")
        capsules = list(data.values()) if isinstance(data, dict) else []
        sorted_capsules = sorted(capsules, key=lambda x: x.get("timestamp", ""), reverse=True)
        return sorted_capsules[:limit]
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "capsule_memory",
            "reflection": "Capsule read failed.",
            "insight": str(e)
        })
        return []

# Retrieve a capsule by its index from recent list
def load_capsule_by_index(index=0):
    try:
        recent = list_capsules(limit=index + 1)
        return recent[index] if index < len(recent) else None
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "capsule_memory",
            "reflection": "Capsule load failed.",
            "insight": str(e)
        })
        return None