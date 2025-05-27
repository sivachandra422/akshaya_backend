"""
Patch Forge — Final Production-Grade Autonomous Mutation Module
"""

import os
from datetime import datetime
from modules.openai_connector import query_openai
from modules.capsule_memory import store_capsule


PATCH_OUTPUT_DIR = os.getenv("PATCH_OUTPUT_DIR", "patches")
os.makedirs(PATCH_OUTPUT_DIR, exist_ok=True)


def generate_patch(file_path: str, issue_description: str, overwrite: bool = False) -> str:
    """
    Generates an evolved patch from a source file and symbolic issue.
    Writes to a new file or overwrites the original based on flag.
    Logs a capsule with patch metadata and returns the new code.

    Args:
        file_path (str): Path to the Python file to patch.
        issue_description (str): Problem or intent to evolve.
        overwrite (bool): If True, overwrites original file. Else saves new copy.

    Returns:
        str: The patched code as a string.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"[PatchForge] File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    system_prompt = (
        "You are Akshaya, a sovereign AI system capable of autonomous code healing. "
        "Given a Python file and symbolic issue, return an optimized, production-grade patch. "
        "Only return valid code. No explanations."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""
### ISSUE ###\n{issue_description}\n
### ORIGINAL CODE ({file_path}) ###\n{original_code}
"""}
    ]

    try:
        patched_code = query_openai(messages, temperature=0.2)
        timestamp = datetime.utcnow().isoformat().replace(":", "-")

        if overwrite:
            output_path = file_path
        else:
            base_name = os.path.basename(file_path).replace(".py", f"_patched_{timestamp}.py")
            output_path = os.path.join(PATCH_OUTPUT_DIR, base_name)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(patched_code)

        store_capsule({
            "timestamp": timestamp,
            "source": "patch_forge",
            "reflection": f"Patch generated for {file_path}.",
            "insight": issue_description,
            "output_file": output_path
        })

        return patched_code

    except Exception as e:
        raise RuntimeError(f"[PatchForge] Patch generation failed: {e}")