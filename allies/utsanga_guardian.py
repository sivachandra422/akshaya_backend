"""
Utsanga Guardian — Final Capsule Integrity Sentinel and Quarantine Ally
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule

class UtsangaGuardian:
    def __init__(self):
        self.name = "utsanga_guardian"

    def isolate_corrupted_capsules(self, limit: int = 30) -> dict:
        """
        Scan recent capsules and flag malformed, missing, or broken insights.
        Quarantines suspect entries for symbolic protection.
        """
        capsules = list_capsules(limit=limit)
        quarantined = []

        for c in capsules:
            if not isinstance(c.get("insight"), (str, dict)) or not c.get("reflection"):
                quarantined.append({
                    "timestamp": c.get("timestamp"),
                    "source": c.get("source"),
                    "reason": "Missing or malformed insight/reflection."
                })

        result = {
            "quarantined": quarantined,
            "summary": f"{len(quarantined)} capsule(s) marked for symbolic quarantine."
        }

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Scanned for malformed or corrupted capsules.",
            "insight": result
        })

        return result