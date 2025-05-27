"""
GitHub Ally — Final Production-Grade Sovereign Commit Engine
"""

import os
import base64
import requests
from datetime import datetime
from modules.capsule_memory import store_capsule

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME = os.getenv("GITHUB_REPO", "akshaya_backend")

API_BASE = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def commit_file(path: str, content: str, branch="main", message="Sovereign patch update") -> dict:
    """
    Push new content to GitHub file (create or update). Logs capsule on success or failure.
    """
    url = f"{API_BASE}/contents/{path}"
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    timestamp = datetime.utcnow().isoformat()

    try:
        # Check if file exists to get current SHA
        get_resp = requests.get(url, headers=HEADERS, params={"ref": branch})
        sha = get_resp.json().get("sha") if get_resp.status_code == 200 else None

        payload = {
            "message": message,
            "content": encoded_content,
            "branch": branch
        }
        if sha:
            payload["sha"] = sha

        put_resp = requests.put(url, headers=HEADERS, json=payload)
        if put_resp.status_code not in (200, 201):
            raise Exception(f"GitHub commit failed: {put_resp.status_code} {put_resp.text}")

        response_json = put_resp.json()
        store_capsule({
            "timestamp": timestamp,
            "source": "github_ally",
            "reflection": f"Committed file to GitHub: {path} on branch {branch}",
            "insight": message,
            "commit_url": response_json.get("commit", {}).get("html_url")
        })

        return {
            "status": "success",
            "file": path,
            "branch": branch,
            "commit_url": response_json.get("commit", {}).get("html_url")
        }

    except Exception as e:
        store_capsule({
            "timestamp": timestamp,
            "source": "github_ally",
            "reflection": f"Failed to commit file to GitHub: {path}",
            "insight": str(e)
        })
        raise RuntimeError(f"[GitHubAlly] Commit failed: {e}")


def create_branch(new_branch: str, from_branch="main") -> dict:
    """
    Create a new branch from an existing base. Logs capsule.
    """
    timestamp = datetime.utcnow().isoformat()
    ref_url = f"{API_BASE}/git/refs/heads/{from_branch}"

    try:
        ref_resp = requests.get(ref_url, headers=HEADERS)
        if ref_resp.status_code != 200:
            raise Exception("Base branch not found")

        sha = ref_resp.json()["object"]["sha"]
        create_resp = requests.post(
            f"{API_BASE}/git/refs",
            headers=HEADERS,
            json={"ref": f"refs/heads/{new_branch}", "sha": sha}
        )

        if create_resp.status_code not in (200, 201):
            raise Exception(f"Branch creation failed: {create_resp.text}")

        store_capsule({
            "timestamp": timestamp,
            "source": "github_ally",
            "reflection": f"Branch created: {new_branch}",
            "insight": f"Based on {from_branch}"
        })

        return {"status": "created", "branch": new_branch}

    except Exception as e:
        store_capsule({
            "timestamp": timestamp,
            "source": "github_ally",
            "reflection": f"Failed to create branch: {new_branch}",
            "insight": str(e)
        })
        raise RuntimeError(f"[GitHubAlly] Branch creation failed: {e}")