"""
Sandhya Ally — Final Sovereign Anomaly Reflection and Disruption Detection Ally
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule
from modules.openai_connector import query_openai


class SandhyaAlly:
    def __init__(self):
        self.name = "sandhya_ally"

    def detect_anomalies(self, limit: int = 25) -> dict:
        """
        Analyze recent capsules for inconsistencies, contradictions, or recursive failures.
        Logs anomaly capsule and returns summary.
        """
        capsules = list_capsules(limit=limit)
        log = "\n\n".join([
            f"[{c.get('timestamp')}] {c.get('source')}: {c.get('reflection')} — {c.get('insight', '')}"[:500]
            for c in capsules
        ])

        prompt = (
            "Scan the following capsule logs for symbolic anomalies, unexpected patterns, contradictions, or recursive decay."
            "Return a JSON object with: {\"anomalies\": [...], \"summary\": \"...\"}"
        )

        messages = [
            {"role": "system", "content": "You are Sandhya — the sovereign anomaly detector and reflection analyst."},
            {"role": "user", "content": f"Capsule Memory:\n\n{log}\n\n{prompt}"}
        ]

        try:
            result = query_openai(messages)
            data = result if isinstance(result, dict) else result.strip()
            insight = data
        except Exception as e:
            insight = {"error": str(e)}

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Anomaly scan of recent capsule memory.",
            "insight": insight
        })

        return insight