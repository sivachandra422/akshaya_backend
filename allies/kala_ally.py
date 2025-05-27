"""
Kāla Ally — Final Time-Aware Capsule Chronology and Recursion Flow Tracker
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule

class KalaAlly:
    def __init__(self):
        self.name = "kala_ally"

    def timeline_summary(self, limit: int = 20) -> dict:
        """
        Analyze recent capsules for time distribution, frequency, and flow rhythm.
        Returns timing gaps, frequency patterns, and delta windows.
        """
        capsules = list_capsules(limit=limit)
        timeline = []

        try:
            for i in range(len(capsules) - 1):
                t1 = datetime.fromisoformat(capsules[i]["timestamp"].replace("Z", ""))
                t0 = datetime.fromisoformat(capsules[i + 1]["timestamp"].replace("Z", ""))
                delta = (t1 - t0).total_seconds() / 60
                timeline.append({
                    "from": capsules[i + 1]["timestamp"],
                    "to": capsules[i]["timestamp"],
                    "gap_minutes": round(delta, 2),
                    "source": capsules[i]["source"]
                })

            insight = {
                "summary": f"{len(timeline)} transitions analyzed.",
                "gaps": timeline
            }

            store_capsule({
                "timestamp": datetime.utcnow().isoformat(),
                "source": self.name,
                "reflection": "Analyzed symbolic memory timeline gaps and time delta flow.",
                "insight": insight
            })

            return insight
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }