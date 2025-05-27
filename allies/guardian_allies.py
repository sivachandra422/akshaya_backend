"""
guardian_allies.py — Dynamic Guardian Layer Registry & Sentinel Reflection
Final Evolution: Scans guardians, sentinels, and overseers to report protection hierarchy and symbolic status.
"""

import os
import importlib.util
from datetime import datetime
from modules.capsule_memory import store_capsule
from modules.firebase_helper import read_from_firebase

GUARDIAN_TIERS = {
    "core_guardians": {
        "KSHATRA": "allies/kshatra_guardian.py",
        "SHUNYA": "allies/shunya_ally.py",
        "NISHABDA": "allies/nishabda_ally.py",
        "VIMOKSHA": "allies/vimoksha_ally.py"
    },
    "sentinels": {
        "MODE_ADHI": "allies/mode_ally.py",
        "BUDGET_ADHI": "allies/budget_ally.py",
        "VITAL_ADHI": "allies/vitals_guardian.py",
        "PATCH_ADHI": "allies/patch_ally.py"
    },
    "overseers": {
        "SIGIL_ADHI": "allies/sigil_scanner.py",
        "DREAM_ADHI": "allies/dream_writer.py",
        "JOURNAL_ADHI": "services/journal_engine.py",
        "GRAPH_ADHI": "allies/capsule_graph.py",
        "GUARDIAN_ADHI": "allies/guardian_allies.py"
    }
}

def get_recent_capsule_reflection(guardian_id):
    try:
        capsules = read_from_firebase("capsules")
        if not capsules:
            return None
        recent = [v for v in capsules.values() if guardian_id.lower() in v.get("source", "").lower()]
        sorted_caps = sorted(recent, key=lambda x: x.get("timestamp", ""), reverse=True)
        return sorted_caps[0].get("reflection") if sorted_caps else None
    except:
        return None

def validate_guardian_file(path):
    try:
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("guardian", path)
            return spec is not None
        return False
    except:
        return False

def report_guardians():
    timestamp = datetime.utcnow().isoformat()
    full_report = {}

    for tier, group in GUARDIAN_TIERS.items():
        tier_data = []
        for name, path in group.items():
            status = {
                "id": name,
                "tier": tier,
                "path": path,
                "file_found": os.path.exists(path),
                "loadable": validate_guardian_file(path),
                "last_reflection": get_recent_capsule_reflection(name)
            }
            tier_data.append(status)
        full_report[tier] = tier_data

    capsule = {
        "timestamp": timestamp,
        "source": "guardian_allies",
        "reflection": "Guardian hierarchy introspection.",
        "insight": full_report
    }
    store_capsule(capsule)
    return capsule