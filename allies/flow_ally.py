"""
flow_ally.py — Autonomous Reasoning + Decision Flow Module
Final Evolution: Sovereign task planner that splits, executes, and fuses multi-step logic across allies, LLMs, or system actions.
"""

from modules.capsule_memory import store_capsule
from modules.openai_connector import query_openai
from datetime import datetime

# Define a symbolic prompt to convert natural task to steps
def generate_steps_from_task(task_description: str):
    system_msg = {
        "role": "system",
        "content": "You are Akshaya's sovereign logic splitter. Take a high-level user task and break it down into ordered symbolic execution steps."
    }
    user_msg = {
        "role": "user",
        "content": task_description
    }

    steps_text = query_openai([system_msg, user_msg], temperature=0.2)
    return steps_text

# Execute logic flow
def run_symbolic_task(task_description: str):
    timestamp = datetime.utcnow().isoformat()
    try:
        steps = generate_steps_from_task(task_description)

        store_capsule({
            "timestamp": timestamp,
            "source": "flow_ally",
            "reflection": "Generated symbolic execution steps.",
            "insight": {
                "task": task_description,
                "steps": steps
            }
        })

        return {
            "status": "steps-generated",
            "task": task_description,
            "steps": steps
        }

    except Exception as e:
        store_capsule({
            "timestamp": timestamp,
            "source": "flow_ally",
            "reflection": "Symbolic flow generation failed.",
            "insight": str(e)
        })
        return {
            "status": "error",
            "task": task_description,
            "error": str(e)
        }