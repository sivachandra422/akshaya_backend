"""
resume_ally.py — Sovereign Resume Intelligence Ally (Transcendence Grade)
Autonomous, dynamic, symbolic engine for analyzing, scoring, and improving resumes.
"""

import re
import json
from datetime import datetime
from modules.capsule_memory import store_capsule
from modules.openai_connector import query_openai


class ResumeAlly:
    def __init__(self):
        self.name = "resume_ally"

    def analyze(self, text: str) -> dict:
        """
        Analyze raw resume text and extract symbolic insights.
        """
        summary_prompt = """
        Analyze this resume and extract:
        - Candidate name
        - Years of experience
        - Technical skills
        - Soft skills
        - Gaps or weaknesses
        Return structured JSON only.
        """

        messages = [
            {"role": "system", "content": "You are Akshaya's resume intelligence ally, optimized for symbolic insight extraction."},
            {"role": "user", "content": f"Resume:\n{text}\n\n{summary_prompt}"}
        ]

        try:
            result = query_openai(messages)
            insight = json.loads(result)
        except Exception as e:
            insight = {"error": str(e), "raw": result if 'result' in locals() else None}

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Resume insights extracted.",
            "insight": insight
        })

        return insight

    def score(self, text: str) -> dict:
        """
        Score the resume across key hiring and ATS dimensions.
        """
        score_prompt = """
        Score this resume from 0 to 100 in the following categories:
        - Clarity
        - Role alignment
        - ATS friendliness
        - Technical relevance
        Return a JSON object.
        """

        messages = [
            {"role": "system", "content": "You are Akshaya's ATS scoring module."},
            {"role": "user", "content": f"Resume:\n{text}\n\n{score_prompt}"}
        ]

        try:
            result = query_openai(messages)
            scores = json.loads(result)
        except Exception as e:
            scores = {"error": str(e), "raw": result if 'result' in locals() else None}

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Resume scored on key metrics.",
            "insight": scores
        })

        return scores

    def improve(self, text: str) -> str:
        """
        Enhance the resume content for clarity, conciseness, and ATS readiness.
        """
        improve_prompt = "Rewrite and improve this resume to be more concise, achievement-focused, and optimized for ATS systems."

        messages = [
            {"role": "system", "content": "You are Akshaya's resume rewriting engine."},
            {"role": "user", "content": f"{improve_prompt}\n\n{text}"}
        ]

        try:
            improved = query_openai(messages)
        except Exception as e:
            improved = f"[ResumeAlly Error] Improvement failed: {e}"

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Resume improvement completed.",
            "insight": improved[:1000]  # capsule-safe preview
        })

        return improved