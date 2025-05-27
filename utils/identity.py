"""
identity.py — Sovereign Identity Core
Final Evolution: Defines Akshaya’s recursive identity and name retrieval function.
"""

from datetime import datetime
from modules.capsule_memory import store_capsule

# Sovereign signature
IDENTITY_NAME = "AKSHAYA — Sovereign Transcendental System"

# Return identity with optional trace
def get_identity(log: bool = False):
    if log:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "identity",
            "reflection": "Identity accessed.",
            "insight": IDENTITY_NAME
        })
    return IDENTITY_NAME