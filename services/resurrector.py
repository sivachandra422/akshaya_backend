"""
Resurrector — Final Sovereign Core for Loop Recovery and System Resurrection
"""

from datetime import datetime
from modules.capsule_memory import list_capsules, store_capsule
from modules.mirror_state import reset_mirror_state, get_mirror_state
from allies.kshatra_guardian import KshatraGuardian
from allies.shunya_ally import ShunyaAlly


class Resurrector:
    def __init__(self):
        self.name = "resurrector"
        self.kshatra = KshatraGuardian()
        self.shunya = ShunyaAlly()

    def scan_and_revive(self) -> dict:
        """
        Detect signs of loop collapse, reflection freeze, or missing memory.
        Trigger recovery logic and log resurrection attempt.
        """
        integrity = self.kshatra.check_environment_integrity()
        silence_check = self.shunya.detect_stillness(threshold_minutes=45)
        mirror = get_mirror_state()

        resurrection_triggered = False
        reason = []

        if integrity.get("sandbox_mode"):
            reason.append("Missing env keys.")
            resurrection_triggered = True

        if "Silent gap" in silence_check.get("status", ""):
            reason.append("Detected memory silence.")
            resurrection_triggered = True

        if mirror.get("status") in ("CRITICAL", "BROKEN"):
            reason.append("Mirror state degraded.")
            resurrection_triggered = True

        if resurrection_triggered:
            reset_mirror_state()
            result = {
                "resurrected": True,
                "reasons": reason,
                "mirror_after": get_mirror_state()
            }
        else:
            result = {
                "resurrected": False,
                "status": "System healthy."
            }

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Checked for recursion breakdown and triggered resurrection if needed.",
            "insight": result
        })

        return result