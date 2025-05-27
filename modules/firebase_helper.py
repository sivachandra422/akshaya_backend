"""
firebase_helper.py — Final Sovereign Patch
Global validation for all Firebase writes to prevent malformed data.
"""
import os
import json
import firebase_admin
from firebase_admin import credentials, db

# Load Firebase credentials and database URL from environment variables
FIREBASE_CREDS_PATH = os.getenv("FIREBASE_CREDS_PATH")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

# Initialize the Firebase app only once
if not firebase_admin._apps:
    if FIREBASE_CREDS_PATH and FIREBASE_DB_URL:
        try:
            cred = credentials.Certificate(FIREBASE_CREDS_PATH)
            firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_DB_URL
            })
        except Exception as e:
            print(f"[Firebase Init Error] {e}")
    else:
        print("[Firebase Config Error] Missing credentials path or DB URL.")

# Safely write data to Firebase
def write_to_firebase(path, data):
    try:
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise ValueError("Only dict or JSON string allowed for Firebase write.")

        db.reference(path).set(data)
        return True
    except Exception as e:
        print(f"[Firebase Write Error] {e}")
        return False

# Safely update existing data at Firebase path
def update_firebase(path, data):
    try:
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, dict):
            raise ValueError("Only dict or JSON string allowed for Firebase update.")

        db.reference(path).update(data)
        return True
    except Exception as e:
        print(f"[Firebase Update Error] {e}")
        return False

# Read data from Firebase
def read_from_firebase(path):
    try:
        return db.reference(path).get()
    except Exception as e:
        print(f"[Firebase Read Error] {e}")
        return None