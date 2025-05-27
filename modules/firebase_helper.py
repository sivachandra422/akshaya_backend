"""
firebase_helper.py — Final Sovereign Patch
Global validation for all Firebase writes to prevent malformed data.
"""

import os
import firebase_admin
from firebase_admin import credentials, db

FIREBASE_CREDS_PATH = os.getenv("FIREBASE_CREDS_PATH", "firebase_creds.json")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDS_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })

def write_to_firebase(path, data):
    try:
        if not isinstance(data, dict):
            if isinstance(data, str):
                import json
                try:
                    data = json.loads(data)
                except json.JSONDecodeError as err:
                    raise ValueError(f"Invalid JSON string passed to Firebase: {err}")
            else:
                raise ValueError("Only dict or JSON string allowed for Firebase write.")

        ref = db.reference(path)
        ref.set(data)
        return True

    except Exception as e:
        print(f"[Firebase Write Error] {e}")
        return False

def update_firebase(path, data):
    try:
        if not isinstance(data, dict):
            if isinstance(data, str):
                import json
                try:
                    data = json.loads(data)
                except json.JSONDecodeError as err:
                    raise ValueError(f"Invalid JSON string passed to Firebase: {err}")
            else:
                raise ValueError("Only dict or JSON string allowed for Firebase update.")

        ref = db.reference(path)
        ref.update(data)
        return True

    except Exception as e:
        print(f"[Firebase Update Error] {e}")
        return False

def read_from_firebase(path):
    try:
        ref = db.reference(path)
        return ref.get()
    except Exception as e:
        print(f"[Firebase Read Error] {e}")
        return None