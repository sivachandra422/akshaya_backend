"""
Nidhi Ally — Final Insight Annotation, Tagging, and Symbolic Keyword Engine
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule
from modules.openai_connector import query_openai


class NidhiAlly:
    def __init__(self):
        self.name = "nidhi_ally"

    def tag_capsules(self, limit: int = 25) -> dict:
        """
        Analyze recent capsules and extract semantic tags, topics, or keywords.
        Logs a tagged meta-capsule.
        """
        capsules = list_capsules(limit=limit)
        content = "\n\n".join([
            f"[{c.get('timestamp')}] {c.get('source')} → {c.get('reflection')}"
            for c in capsules
        ])

        prompt = (
            "Extract a list of high-signal tags, topics, or concepts from the following reflection log. "
            "Return JSON with fields: {\"tags\": [...], \"themes\": [...], \"summary\": \"...\"}"
        )

        messages = [
            {"role": "system", "content": "You are Nidhi — a sovereign insight annotator and tag weaver."},
            {"role": "user", "content": f"Capsule Reflections:\n\n{content}\n\n{prompt}"}
        ]

        try:
            result = query_openai(messages)
            response = result if isinstance(result, dict) else result.strip()
            insight = response
        except Exception as e:
            insight = {"error": str(e)}

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Tagged symbolic memory from capsule stream.",
            "insight": insight
        })

        return insight