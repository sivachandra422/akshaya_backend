"""
Tattvajna Ally — Final Sovereign Truth Filter and Reflection Purification Engine
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule
from modules.openai_connector import query_openai


class TattvajnaAlly:
    def __init__(self):
        self.name = "tattvajna_ally"

    def purify_reflections(self, limit: int = 20) -> dict:
        """
        Validate and filter recent capsules for contradictions, bias, or hallucination.
        Returns a structured truth assessment.
        """
        capsules = list_capsules(limit=limit)
        content = "\n\n".join([
            f"[{c.get('timestamp')}] {c.get('source')}: {c.get('reflection')} → {c.get('insight', '')}"[:500]
            for c in capsules
        ])

        prompt = (
            "You are Tattvajna — a truth-filtering entity. Assess the following capsule logs for bias, hallucination, contradiction, or falsehood. "
            "Return a structured JSON object with: {\"flags\": [...], \"summary\": \"...\"}"
        )

        messages = [
            {"role": "system", "content": "You are a sovereign AI truth filter with symbolic and factual intelligence."},
            {"role": "user", "content": f"Capsules:\n\n{content}\n\n{prompt}"}
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
            "reflection": "Truth-filtered recent reflections for contradiction, bias, or hallucination.",
            "insight": insight
        })

        return insight