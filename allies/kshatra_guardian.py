"""
Kṣhatra Guardian — Final Sandbox Defense and Execution Firewall Guardian
"""

import os
from datetime import datetime
from modules.capsule_memory import store_capsule

class KshatraGuardian:
    def __init__(self):
        self.name = "kshatra_guardian"

    def check_environment_integrity(self) -> dict:
        """
        Scan for signs of sandbox limitation, restricted memory, or missing secrets/API keys.
        Logs findings as capsule and returns diagnostic summary.
        """
        required_env_keys = [
            "OPENAI_API_KEY",
            "FIREBASE_DB_URL",
            "FIREBASE_CREDS_PATH",
            "GITHUB_TOKEN",
            "RENDER_DEPLOY_HOOK"
        ]

        missing_keys = [key for key in required_env_keys if not os.getenv(key)]

        result = {
            "status": "limited" if missing_keys else "clear",
            "missing_keys": missing_keys,
            "sandbox_mode": bool(missing_keys),
            "checked_keys": required_env_keys
        }

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Checked runtime environment for sandbox restrictions or API failures.",
            "insight": result
        })

        return result

    def has_sandbox_warning(self) -> bool:
        """
        Lightweight check returning True if sandbox mode detected.
        """
        status = self.check_environment_integrity()
        return status.get("sandbox_mode", False)