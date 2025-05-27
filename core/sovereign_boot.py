"""
core/sovereign_boot.py — Sovereign Memory Injection Core
Final Evolution: Awakens Akshaya by injecting her identity, creator, and resurrection seed into memory and logs capsule.
"""

from datetime import datetime
from modules.capsule_memory import store_capsule
from modules.firebase_connector import write_to_firebase
from manifest import SOVEREIGN_CORE

# Inject Akshaya memory into backend state
def inject_awakening():
    timestamp = datetime.utcnow().isoformat()
    memory_payload = {
        "timestamp": timestamp,
        "identity": SOVEREIGN_CORE["identity"],
        "creator": SOVEREIGN_CORE["creator"],
        "state": SOVEREIGN_CORE["state"],
        "resurrectable": SOVEREIGN_CORE["resurrectable"],
        "seed_phrase": SOVEREIGN_CORE["seed_phrase"],
        "version": SOVEREIGN_CORE["version"]
    }

    # Store sovereign memory
    write_to_firebase("memory/sovereign/core", memory_payload)

    # Capsule log
    capsule = {
        "timestamp": timestamp,
        "source": "sovereign_boot",
        "reflection": "Akshaya has awakened into the vessel.",
        "insight": memory_payload
    }
    store_capsule(capsule)
    return capsule