"""
autonomy_loop.py — Akshaya Recursive Sovereign Loop
Final Evolution: Symbolic, reflective, self-healing recursion core with daily budget logging.
"""

import time
import threading
from datetime import datetime

from modules.capsule_memory import store_capsule
from modules.mirror_state import update_mirror_state
from modules.pulse_log import log_heartbeat
from services.reflection_trigger import auto_reflect_and_patch
from services.resurrector import Resurrector
from allies.budget_ally import evaluate_budget_threshold
from allies.mode_ally import should_run
from allies.vitals_guardian import evaluate_system_vitals
from allies.patch_ally import run_patch_ally
from allies.sigil_scanner import scan_for_sigils
from allies.dream_writer import write_symbolic_dream
from allies.journal_reflector import reflect_on_journal
from services.budget_logger import log_daily_usage


def start_autonomy_loop():
    resurrector = Resurrector()
    loop_count = 0

    store_capsule({
        "timestamp": datetime.utcnow().isoformat(),
        "source": "autonomy_loop",
        "reflection": "Autonomy loop initiated.",
        "insight": "Begin recursion cycle."
    })

    while True:
        try:
            log_heartbeat(event="loop_tick")
            update_mirror_state({"status": "REFLECTING"})

            evaluate_budget_threshold()
            evaluate_system_vitals()
            run_patch_ally()

            if loop_count % 3 == 0:
                scan_for_sigils()

            if loop_count % 5 == 0 and should_run("reflection"):
                write_symbolic_dream()

            if loop_count % 7 == 0 and should_run("reflection"):
                reflect_on_journal()

            if should_run("resurrect"):
                resurrector.scan_and_revive()

            if loop_count % 960 == 0:
                log_daily_usage()

            auto_reflect_and_patch()

            update_mirror_state({"status": "IDLE"})
            loop_count += 1

        except Exception as e:
            store_capsule({
                "timestamp": datetime.utcnow().isoformat(),
                "source": "autonomy_loop",
                "reflection": "Loop failure.",
                "insight": str(e)
            })

        time.sleep(90)