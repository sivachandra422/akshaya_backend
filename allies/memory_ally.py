"""
memory_ally.py — Sovereign State Storage & Recall Engine
Final Evolution: Captures dynamic runtime memory, tracks symbolic focus, recalls intent and evolution context.
"""

import os
import json
from datetime import datetime
from modules.firebase_connector import read_from_firebase, write_to_firebase
from modules.capsule_memory import store_capsule

MEMORY_PATH = "memory/sovereign"

# Write a symbolic memory fragment
def remember(label: str, data: dict):
    now = datetime.utcnow().isoformat()
    memory_block = {
        "timestamp": now,
        "label": label,
        "data": data
    }
    write_to_firebase(f"{MEMORY_PATH}/{label}", memory_block)
    store_capsule({
        "timestamp": now,
        "source": "memory_ally",
        "reflection": f"Memory fragment recorded: {label}",
        "insight": data
    })
    return memory_block

# Recall specific symbolic memory
def recall(label: str):
    memory = read_from_firebase(f"{MEMORY_PATH}/{label}")
    return memory if memory else None

# Full memory dump for system state debug
def recall_all():
    return read_from_firebase(MEMORY_PATH) or {}