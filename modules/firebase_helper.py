"""
firebase_helper.py — Realtime Database Helper for Firebase
Final patch: Strict validation for JSON data and defensive error catching
"""

import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

load_dotenv()

FIREBASE_CREDENTIAL_PATH = os.getenv("FIREBASE_CREDS_PATH")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIAL_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })


def write_to_firebase(path: str, data):
    try:
        if not isinstance(data, dict):
            if isinstance(data, str):
                if not data.strip():
                    raise ValueError("Empty string is not valid JSON data for Firebase.")
                import json
                try:
                    data = json.loads(data)
                except Exception as parse_err:
                    raise ValueError(f"Failed to parse JSON string: {parse_err}")
            else:
                raise ValueError("Unsupported data type for Firebase write.")

        ref = db.reference(path)
        ref.set(data)
        print(f"[Firebase] Wrote to {path}: {data}")
    except Exception as e:
        print(f"[Firebase Write Error] Path: {path}, Data: {data}, Error: {e}")


def update_firebase(path: str, data):
    try:
        if not isinstance(data, dict):
            if isinstance(data, str):
                if not data.strip():
                    raise ValueError("Empty string is not valid JSON data for Firebase.")
                import json
                try:
                    data = json.loads(data)
                except Exception as parse_err:
                    raise ValueError(f"Failed to parse JSON string: {parse_err}")
            else:
                raise ValueError("Unsupported data type for Firebase update.")

        db.reference(path).push(data)
        print(f"[Firebase] Updated {path} with: {data}")
    except Exception as e:
        print(f"[Firebase Update Error] Path: {path}, Data: {data}, Error: {e}")