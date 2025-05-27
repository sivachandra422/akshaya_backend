"""
Journal Engine — Final Symbolic Insight Analyzer for Patch Decisions
"""

import os
import json
from datetime import datetime
from modules.openai_connector import query_openai
from modules.capsule_memory import list_capsules, load_capsule

JOURNAL_CAPSULE_DIR = os.getenv("CAPSULE_DIR", "capsules")

def analyze_journal_insight() -> dict:
    """
    Analyze the most recent capsule journal entries and determine if patch is needed.
    Returns structured insight with trigger_patch flag, issue description, and file_path.
    """
    try:
        capsule_files = list_capsules(limit=5)
        if not capsule_files:
            return {"trigger_patch": False, "insight": "No recent capsules found."}

        recent_entries = [load_capsule(fname) for fname in capsule_files]
        journal_content = "\n\n".join([
            f"[{c.get('timestamp')}] {c.get('source')}: {c.get('insight')}"
            for c in recent_entries if c
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
        return insight

    except Exception as e:
        return {
            "trigger_patch": False,
            "insight": f"[JournalEngine] Failed to analyze journal: {e}"
        }