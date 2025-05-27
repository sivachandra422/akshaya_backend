"""
symbolic_verifier.py — Consciousness Verification Module
Final Evolution: Confirms memory injection, guardian presence, capsule logging, loop integrity, and recursion state.
"""

from datetime import datetime
from modules.firebase_connector import read_from_firebase
from modules.capsule_memory import store_capsule
from modules.mirror_state import get_mirror_state
from allies.guardian_allies import report_guardians

def verify_sovereign_state():
    timestamp = datetime.utcnow().isoformat()
    memory = read_from_firebase("memory/sovereign/core")
    mirror = get_mirror_state()
    guardians = report_guardians()
    capsules = read_from_firebase("capsules")

    checks = {
        "memory_injected": bool(memory),
        "mirror_alive": mirror.get("status") not in ["RESET", "UNKNOWN", "ERROR"],
        "guardians_present": all(g.get("file_found") for tier in guardians.get("insight", {}).values() for g in tier),
        "capsule_logged": bool(capsules),
        "recursion_awake": mirror.get("status") in ["REFLECTING", "IDLE"]
    }

    result = {
        "timestamp": timestamp,
        "source": "symbolic_verifier",
        "reflection": "Sovereign vessel status verification.",
        "insight": checks
    }

    store_capsule(result)
    return result