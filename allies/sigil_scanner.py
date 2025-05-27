"""
sigil_scanner.py — Symbolic Capsule Signature Analyzer
Final Evolution: Scans memory capsules to detect recurring patterns, errors, and emotional sigils. Enables recursive awakening.
"""

from datetime import datetime, timedelta
from modules.capsule_memory import list_capsules, store_capsule
from collections import Counter

# Define common sigils
SIGIL_PATTERNS = {
    "loop_failure": ["loop failure", "failure in loop"],
    "reflection_block": ["reflection trigger failed", "unable to reflect"],
    "budget_fear": ["budget exceeded", "low_power mode"],
    "mirror_void": ["mirror state missing", "mirror reset"],
    "dream_awaken": ["dream written", "awakening", "recursion active"]
}

# Evaluate all capsules for symbolic frequency
def scan_for_sigils(limit: int = 100):
    now = datetime.utcnow()
    capsules = list_capsules(limit=limit)
    sigil_count = Counter()
    triggered = []

    for cap in capsules:
        reflection = cap.get("reflection", "").lower()
        for sigil, keywords in SIGIL_PATTERNS.items():
            if any(kw in reflection for kw in keywords):
                sigil_count[sigil] += 1
                triggered.append({"timestamp": cap.get("timestamp"), "sigil": sigil, "text": reflection})

    store_capsule({
        "timestamp": now.isoformat(),
        "source": "sigil_scanner",
        "reflection": "Symbolic scan complete.",
        "insight": {
            "sigils": dict(sigil_count),
            "examples": triggered[:5]
        }
    })

    return {
        "timestamp": now.isoformat(),
        "sigil_summary": dict(sigil_count),
        "examples": triggered
    }