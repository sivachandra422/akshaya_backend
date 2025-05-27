"""
firebase_connector.py — Sovereign Firebase Adapter (Final Evolution)
All Firebase operations routed through firebase_helper. No SDK, no circular logic.
"""

from datetime import datetime
from modules.firebase_helper import read_from_firebase, update_firebase

def append_to_firebase(path: str, data: dict):
    try:
        timestamp = datetime.utcnow().isoformat()
        safe_key = timestamp.replace(":", "-").replace(".", "-")
        payload = {safe_key: data}
        update_firebase(path, payload)
        return True
    except Exception as e:
        print(f"[Firebase Append Error] {e}")
        return False

def read_all_from_firebase(path: str):
    try:
        return read_from_firebase(path)
    except Exception as e:
        print(f"[Firebase Read Error] {e}")
        return None

def update_field(path: str, key: str, value):
    try:
        safe_key = str(key).replace(":", "-").replace(".", "-")
        update_firebase(path, {safe_key: value})
        return True
    except Exception as e:
        print(f"[Firebase Field Update Error] {e}")
        return False