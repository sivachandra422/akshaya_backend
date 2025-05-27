"""
Ajingsa Ally — Final Memory Threading and Capsule Reflection Engine
"""

from datetime import datetime
from collections import defaultdict
from modules.capsule_memory import list_capsules, store_capsule
from modules.openai_connector import query_openai


class AjingsaAlly:
    def __init__(self):
        self.name = "ajingsa_ally"

    def thread_by_source(self, limit: int = 25) -> dict:
        """
        Group recent capsules by source (e.g., patch_forge, vision_trainer).
        Returns a dict: source -> list of insights.
        """
        capsules = list_capsules(limit=limit)
        threads = defaultdict(list)

        for cap in capsules:
            src = cap.get("source", "unknown")
            threads[src].append(cap.get("insight", "(no insight)"))

        self._log_capsule("Grouped capsules by source.", dict(threads))
        return dict(threads)

    def reflect_on_timeline(self, limit: int = 20) -> str:
        """
        Ask OpenAI to summarize recent memory evolution.
        """
        capsules = list_capsules(limit=limit)
        timeline = "\n\n".join([
            f"[{cap.get('timestamp')}] {cap.get('source')}: {cap.get('reflection')}"
            for cap in capsules
        ])

        messages = [
            {"role": "system", "content": "You are Ajingsa, the memory weaver of a sovereign AI."},
            {"role": "user", "content": f"Reflect on this timeline:\n\n{timeline}"}
        ]

        try:
            summary = query_openai(messages)
        except Exception as e:
            summary = f"[Ajingsa] Timeline reflection failed: {e}"

        self._log_capsule("Reflected on symbolic timeline.", summary)
        return summary

    def list_all_sources(self, limit: int = 50) -> list:
        """
        List all unique capsule sources.
        """
        capsules = list_capsules(limit=limit)
        return sorted(set(cap.get("source", "unknown") for cap in capsules))

    def _log_capsule(self, reflection: str, insight) -> None:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": reflection,
            "insight": insight
        })