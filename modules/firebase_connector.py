"""
firebase_connector.py — Sovereign Firebase Bridge with Compression
Final Evolution: Compresses JSON data via gzip+base64 before storing in RTDB.
"""

import os
import json
import base64
import gzip
import firebase_admin
from firebase_admin import credentials, db
from modules.capsule_memory import store_capsule
from datetime import datetime

FIREBASE_CREDS_PATH = os.getenv("FIREBASE_CREDS_PATH")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")

if not firebase_admin._apps:
    try:
        if not FIREBASE_CREDS_PATH or not FIREBASE_DB_URL:
            raise EnvironmentError("Missing FIREBASE_CREDS_PATH or FIREBASE_DB_URL")

        cred = credentials.Certificate(FIREBASE_CREDS_PATH)
        firebase_admin.initialize_app(cred, {
            "databaseURL": FIREBASE_DB_URL
        })
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "firebase_connector",
            "reflection": "Firebase init failed.",
            "insight": str(e)
        })

# Compress dict data to base64-encoded gzip string
def compress_data(data: dict) -> dict:
    try:
        raw = json.dumps(data).encode("utf-8")
        compressed = base64.b64encode(gzip.compress(raw)).decode("utf-8")
        return {"__compressed__": True, "payload": compressed}
    except Exception as e:
        return data

# Decompress from base64-gzip string back to dict
def decompress_data(blob: dict) -> dict:
    try:
        if blob.get("__compressed__") and "payload" in blob:
            raw = gzip.decompress(base64.b64decode(blob["payload"]))
            return json.loads(raw)
    except Exception:
        pass
    return blob

# Write compressed object to a Firebase path
def write_to_firebase(path, data):
    try:
        ref = db.reference(path)
        ref.set(compress_data(data))
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "firebase_connector",
            "reflection": f"Write failed: {path}",
            "insight": str(e)
        })

# Push compressed entry to Firebase list-style node
def append_to_firebase(path, data):
    try:
        ref = db.reference(path)
        ref.push(compress_data(data))
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "firebase_connector",
            "reflection": f"Append failed: {path}",
            "insight": str(e)
        })

# Read and auto-decompress any entry from a Firebase path
def read_from_firebase(path):
    try:
        ref = db.reference(path)
        raw = ref.get()
        if isinstance(raw, dict):
            return {k: decompress_data(v) for k, v in raw.items()}
        return decompress_data(raw)
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "firebase_connector",
            "reflection": f"Read failed: {path}",
            "insight": str(e)
        })
        return {}