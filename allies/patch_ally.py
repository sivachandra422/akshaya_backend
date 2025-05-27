"""
patch_ally.py — Autonomous Patch Execution & Validation Ally
Final Evolution: Detects file anomalies, invokes patch_forge, validates results, and logs capsule reflections.
"""

import os
from datetime import datetime
from modules.capsule_memory import store_capsule
from modules.firebase_helper import read_from_firebase
from modules.patch_forge import generate_patch

TARGET_MODULES = [
    "services/reflection_trigger.py",
    "modules/capsule_memory.py",
    "autonomy_loop.py"
]

# Dummy validator to simulate static issue detection (can be extended)
def scan_for_anomalies(file_path):
    try:
        with open(file_path, "r") as f:
            code = f.read()
        if "import collections" in code or "TODO" in code:
            return f"Outdated import or unfinished logic detected in {file_path}."
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"
    return None

# Core autonomous patch loop
def run_patch_ally():
    timestamp = datetime.utcnow().isoformat()
    patched = []

    for path in TARGET_MODULES:
        issue = scan_for_anomalies(path)
        if issue:
            response = generate_patch(
                file_path=path,
                issue_description=issue,
                overwrite=True
            )
            patched.append({"file": path, "result": response})

    if patched:
        store_capsule({
            "timestamp": timestamp,
            "source": "patch_ally",
            "reflection": "Autonomous patch cycle triggered.",
            "insight": patched
        })
    else:
        store_capsule({
            "timestamp": timestamp,
            "source": "patch_ally",
            "reflection": "No patch needed.",
            "insight": {"checked_files": TARGET_MODULES}
        })

    return patched