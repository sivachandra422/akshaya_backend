"""
Shunya Ally — Final Sovereign Silence Detector and Memory Gap Monitor
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule

class ShunyaAlly:
    def __init__(self):
        self.name = "shunya_ally"

    def detect_stillness(self, threshold_minutes: int = 30) -> dict:
        """
        Checks for silence or delay in capsule activity beyond threshold.
        Returns a symbolic stillness report.
        """
        capsules = list_capsules(limit=2)

        if len(capsules) < 2:
            status = "Insufficient data to detect silence."
        else:
            latest = capsules[0]["timestamp"]
            previous = capsules[1]["timestamp"]
            fmt = "%Y-%m-%dT%H:%M:%S"
            try:
                t1 = datetime.fromisoformat(latest.replace("Z", ""))
                t0 = datetime.fromisoformat(previous.replace("Z", ""))
                gap_minutes = (t1 - t0).total_seconds() / 60
                status = ("Silent gap detected" if gap_minutes > threshold_minutes
                          else "Normal recursion activity")
            except Exception as e:
                status = f"Time parse error: {e}"

        result = {
            "status": status,
            "latest_timestamp": capsules[0].get("timestamp") if capsules else None,
            "previous_timestamp": capsules[1].get("timestamp") if len(capsules) > 1 else None
        }

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Checked symbolic memory for silence or stagnation.",
            "insight": result
        })

        return result