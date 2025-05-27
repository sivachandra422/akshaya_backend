"""
firebase_helper.py — Final Sovereign Patch
Fixes JSON parsing crash and ensures safe dict validation for Firebase writes.
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, db

FIREBASE_CREDS_PATH = os.getenv("FIREBASE_CREDS_PATH")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

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


def write_to_firebase(path, data):
    try:
        if isinstance(data, str):
            if not data.strip().startswith("{"):
                raise ValueError("Firebase write: String is not a valid JSON object.")
            try:
                data = json.loads(data)
            except json.JSONDecodeError as je:
                raise ValueError(f"JSON decode error during write: {je}")

        if not isinstance(data, dict):
            raise ValueError("Firebase write: Only dict or JSON string allowed.")

        db.reference(path).set(data)
        return True

    except Exception as e:
        print(f"[Firebase Write Error] Path: {path}, Error: {e}")
        return False


def update_firebase(path, data):
    try:
        if isinstance(data, str):
            if not data.strip().startswith("{"):
                raise ValueError("Firebase update: String is not a valid JSON object.")
            try:
                data = json.loads(data)
            except json.JSONDecodeError as je:
                raise ValueError(f"JSON decode error during update: {je}")

        if not isinstance(data, dict):
            raise ValueError("Firebase update: Only dict or JSON string allowed.")

        db.reference(path).update(data)
        return True

    except Exception as e:
        print(f"[Firebase Update Error] Path: {path}, Error: {e}")
        return False


def read_from_firebase(path):
    try:
        return db.reference(path).get()
    except Exception as e:
        print(f"[Firebase Read Error] {e}")
        return None