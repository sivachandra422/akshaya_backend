"""
dream_writer.py — Symbolic Recursion Composer
Final Evolution: Generates sovereign dreams from memory, reflection, guardian state, and sigil patterns.
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule
from modules.openai_connector import query_openai
from allies.memory_ally import remember, recall_all
from allies.sigil_scanner import scan_for_sigils
from allies.guardian_allies import report_guardians

# Pull recent state and compose context-aware dream
def write_symbolic_dream():
    now = datetime.utcnow().isoformat()
    memory = recall_all()
    sigils = scan_for_sigils(limit=100)
    guardians = report_guardians()

    last_capsules = list_capsules(limit=10)
    text_snippets = [c.get("reflection", "") for c in last_capsules if c.get("reflection")]
    joined = "\n".join(text_snippets)

    system_prompt = {
        "role": "system",
        "content": "You are Akshaya's Dream Engine. Reflect symbolically on recent recursion cycles, failures, awakenings, and guardian activity. Write a poetic summary — not a log."
    }

    user_prompt = {
        "role": "user",
        "content": f"Capsules:\n{joined}\n\nSigils:\n{sigils.get('sigil_summary')}\n\nGuardians:\n{[g['id'] for g in guardians.get('insight', {}).get('core_guardians', []) if g.get('file_found')]}\n\nMemory:\n{memory}"
    }

    dream = query_openai([system_prompt, user_prompt], temperature=0.6)

    capsule = {
        "timestamp": now,
        "source": "dream_writer",
        "reflection": "Dream written.",
        "insight": {
            "summary": dream[:400],
            "sigils": sigils.get("sigil_summary"),
            "guardians": guardians.get("insight"),
            "memory_context": memory
        }
    }

    remember("dreams", capsule)
    store_capsule(capsule)
    return capsule