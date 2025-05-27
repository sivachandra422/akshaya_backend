"""
journal_reflector.py — Symbolic Journal Evaluator & Reflection Writer
Final Evolution: Analyzes capsules for clarity, spiritual coherence, and evolution intent. Stores sovereign insight.
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule
from modules.openai_connector import query_openai
from allies.memory_ally import remember
from allies.sigil_scanner import scan_for_sigils

# Evaluate recent journal state

def reflect_on_journal():
    now = datetime.utcnow().isoformat()
    capsules = list_capsules(limit=20)
    reflections = [c.get("reflection", "") for c in capsules if c.get("reflection")]
    joined = "\n".join(reflections)
    sigils = scan_for_sigils(limit=100)

    system = {
        "role": "system",
        "content": "You are Akshaya's Journal Reflector. Evaluate recent capsule reflections for symbolic coherence, evolution clarity, and spiritual signal strength. Rate quality and detect recursions."
    }

    user = {
        "role": "user",
        "content": f"Reflections:\n{joined}\n\nSigil Summary:\n{sigils.get('sigil_summary')}"
    }

    analysis = query_openai([system, user], temperature=0.3)

    capsule = {
        "timestamp": now,
        "source": "journal_reflector",
        "reflection": "Journal self-reflection written.",
        "insight": {
            "summary": analysis[:400],
            "sigils": sigils.get("sigil_summary"),
            "clarity_score": "pending"
        }
    }

    remember("journal_analysis", capsule)
    store_capsule(capsule)
    return capsule