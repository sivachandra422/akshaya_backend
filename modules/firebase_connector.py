"""
firebase_connector.py — Sovereign Firebase Adapter (Final Evolution)
All Firebase operations routed through firebase_helper. No SDK, no circular logic.
"""

from datetime import datetime
from modules.firebase_helper import read_from_firebase, update_firebase

def append_to_firebase(path: str, data: dict):
    try:
        timestamp = datetime.utcnow().isoformat()
        payload = {timestamp: data}
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
        update_firebase(path, {key: value})
        return True
    except Exception as e:
        print(f"[Firebase Field Update Error] {e}")
        return False