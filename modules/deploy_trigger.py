"""
Deploy Trigger — Render Webhook Invoker for Sovereign Self-Deployment
"""

import os
import requests
from datetime import datetime
from modules.capsule_memory import store_capsule

RENDER_HOOK_URL = os.getenv("RENDER_DEPLOY_HOOK")


def trigger_deploy(source="reflection_trigger") -> dict:
    """
    Triggers a deployment on Render using the configured webhook.
    Logs a capsule with deploy metadata.

    Args:
        source (str): Who initiated the deployment (for tracking).

    Returns:
        dict: Response status or error.
    """
    if not RENDER_HOOK_URL:
        raise EnvironmentError("RENDER_DEPLOY_HOOK not set in environment.")

    try:
        response = requests.post(RENDER_HOOK_URL, timeout=10)
        status = response.status_code

        capsule = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "reflection": "Deployment triggered to Render.",
            "insight": f"HTTP {status}: {response.text[:200]}"
        }
        store_capsule(capsule)

        return {"status": status, "message": response.text.strip()}

    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "reflection": "Deployment failed to trigger.",
            "insight": str(e)
        })
        raise RuntimeError(f"[DeployTrigger