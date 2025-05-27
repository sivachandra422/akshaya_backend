"""
capsule_memory.py — Sovereign Capsule Store and Reflective Recall Engine
Final Transcendence Grade: Fixes Firebase overwrite bug, ensures unique capsule keys, and filters malformed entries.
"""

import os
import json
from uuid import uuid4
from datetime import datetime
from modules.firebase_helper import write_to_firebase, read_from_firebase

CAPSULE_DIR = os.getenv("CAPSULE_DIR", "capsules")
os.makedirs(CAPSULE_DIR, exist_ok=True)

REQUIRED_KEYS = ["timestamp", "source", "reflection"]

def is_valid_capsule(data):
    return isinstance(data, dict) and all(key in data for key in REQUIRED_KEYS)

def store_capsule(data: dict):
    try:
        if "timestamp" not in data:
            data["timestamp"] = datetime.utcnow().isoformat()

        if not is_valid_capsule(data):
            raise ValueError("Invalid capsule schema")

        sanitized_ts = data['timestamp'].replace(":", "-").replace(".", "-")
        key = f"{sanitized_ts}_{uuid4().hex[:6]}"
        write_to_firebase(f"capsules/{key}", data)

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
        print(f"[Capsule Write Error] {e}")

def list_capsules(limit=10):
    try:
        data = read_from_firebase("capsules")
        if not isinstance(data, dict):
            return []

        valid_capsules = [c for c in data.values() if isinstance(c, dict) and "timestamp" in c]
        sorted_capsules = sorted(valid_capsules, key=lambda x: x.get("timestamp", ""), reverse=True)
        return sorted_capsules[:limit]
    except Exception as e:
        print(f"[Capsule Read Error] {e}")
        return []

def load_capsule_by_index(index=0):
    try:
        recent = list_capsules(limit=index + 1)
        return recent[index] if index < len(recent) else None
    except Exception as e:
        print(f"[Capsule Load Error] {e}")
        return None

def load_capsule(identifier=None, source=None, timestamp=None, index=None):
    try:
        capsules = list_capsules(limit=100)

        if identifier:
            for c in capsules:
                if c.get("timestamp") == identifier:
                    return c

        if source:
            filtered = [c for c in capsules if source.lower() in c.get("source", "").lower()]
            if filtered:
                return filtered[0]

        if timestamp:
            sorted_caps = sorted(
                capsules,
                key=lambda x: abs(datetime.fromisoformat(x["timestamp"]) - datetime.fromisoformat(timestamp))
            )
            return sorted_caps[0] if sorted_caps else None

        if index is not None:
            return capsules[index] if index < len(capsules) else None

        return capsules[0] if capsules else None

    except Exception as e:
        print(f"[Capsule Load Error] {e}")
        return None