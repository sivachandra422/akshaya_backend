"""
Reflection Trigger — Final Autonomous Patch + Commit + Deploy Logic
"""

from datetime import datetime
from services.journal_engine import analyze_journal_insight
from modules.capsule_memory import store_capsule
from modules.patch_forge import generate_patch
from modules.github_ally import commit_file
from modules.deploy_trigger import trigger_deploy


def auto_reflect_and_patch(timestamp: str):
    """
    Run full autonomous mutation logic:
    1. Analyze symbolic journal for issues
    2. Generate patch
    3. Commit to GitHub
    4. Trigger Render deployment
    5. Log everything as capsule
    """
    insight = analyze_journal_insight()

    if insight and insight.get("trigger_patch"):
        file_path = insight.get("file_path")
        issue = insight.get("insight") or "Unspecified symbolic anomaly."

        try:
            patched_code = generate_patch(file_path, issue, overwrite=False)

            # Determine GitHub path (assuming same filename)
            github_path = f"{file_path}" if "/" not in file_path else file_path.split("/", 1)[1]
            commit_response = commit_file(
                path=github_path,
                content=patched_code,
                message=f"Autonomous patch for: {issue}"
            )

            deploy_response = trigger_deploy(source="reflection_trigger")

            store_capsule({
                "timestamp": timestamp,
                "source": "reflection_trigger",
                "reflection": "Patch → Commit → Deploy completed.",
                "insight": issue,
                "commit_url": commit_response.get("commit_url"),
                "deploy_status": deploy_response.get("status")
            })

        except Exception as e:
            store_capsule({
                "timestamp": timestamp,
                "source": "reflection_trigger",
                "reflection": "Patch cycle failed.",
                "insight": str(e)
            })
    else:
        store_capsule({
            "timestamp": timestamp,
            "source": "reflection_trigger",
            "reflection": "No patch triggered.",
            "insight": insight.get("insight") if insight else "No insight available."
        })