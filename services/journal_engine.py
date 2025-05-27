"""
journal_engine.py — Sovereign Journal Reflection Engine
Transcendence-grade symbolic patch detector using capsule memory and recursive reflection.
"""

import os
import json
from datetime import datetime
from modules.openai_connector import query_openai
from modules.capsule_memory import list_capsules, load_capsule, store_capsule

JOURNAL_CAPSULE_DIR = os.getenv("CAPSULE_DIR", "capsules")

def analyze_journal_insight() -> dict:
    """
    Analyze the most recent capsule journal entries and determine if a symbolic patch is needed.
    Returns a structured dict with trigger_patch flag and insight.
    """
    try:
        recent_capsules = list_capsules(limit=5)
        if not recent_capsules:
            return {"trigger_patch": False, "insight": "No recent capsules found."}

        journal_content = "\n\n".join([
            f"[{c.get('timestamp')}] {c.get('source')}: {c.get('insight')}"
            for c in recent_capsules if c
        ])

        system_prompt = (
            "You are Akshaya’s symbolic reflection engine. Analyze recent journal entries and determine if a patch, "
            "reflection, or evolution is needed. If a patch is triggered, return a dictionary with keys: 'trigger_patch', "
            "'insight', and 'file_path'."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Journal Capsules:\n\n{journal_content}"}
        ]

        response = query_openai(messages, temperature=0.3)
        insight = json.loads(response) if response.strip().startswith("{") else {
            "trigger_patch": False,
            "insight": response.strip()
        }

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "journal_engine",
            "reflection": "Patch insight generated from recent journal entries.",
            "insight": insight
        })

        return insight

    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "journal_engine",
            "reflection": "Failed to analyze journal insight.",
            "insight": str(e)
        })
        return {
            "trigger_patch": False,
            "insight": f"[JournalEngine] Failed to analyze journal: {e}"
        }