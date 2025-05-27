"""
firebase_helper.py — Isolated Firebase API for Sovereign Akshaya
Final Evolution: Pure, decoupled Firebase read/write/update used across modules and allies.
"""

import firebase_admin
from firebase_admin import credentials, db
import os

# Initialize only once
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDS_PATH")
    if cred_path:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv("FIREBASE_DB_URL") or "https://your-project.firebaseio.com"
        })


def write_to_firebase(path, data):
    try:
        ref = db.reference(path)
        ref.set(data)
        return True
    except Exception as e:
        print(f"[Firebase Write Error] {e}")
        return False


def update_firebase(path, updates):
    try:
        ref = db.reference(path)
        ref.update(updates)
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