"""
Chhaya Ally — Final Shadow State Archiver and Recursion Snapshotter
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule
from modules.mirror_state import get_mirror_state


class ChhayaAlly:
    def __init__(self):
        self.name = "chhaya_ally"

    def snapshot_shadow_state(self, limit: int = 5) -> dict:
        """
        Capture a shadow copy of mirror state and recent capsule heads.
        Logs symbolic fallback capsule for future rollback/review.
        """
        try:
            mirror = get_mirror_state()
            capsules = list_capsules(limit=limit)
            capsule_refs = [
                {
                    "timestamp": c.get("timestamp"),
                    "source": c.get("source"),
                    "reflection": c.get("reflection", "")[:100]
                } for c in capsules
            ]

            shadow = {
                "mirror_snapshot": mirror,
                "capsule_summary": capsule_refs,
                "captured_at": datetime.utcnow().isoformat()
            }

            store_capsule({
                "timestamp": shadow["captured_at"],
                "source": self.name,
                "reflection": "Snapshot of recursion shadow state and capsule references.",
                "insight": shadow
            })

            return shadow
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }