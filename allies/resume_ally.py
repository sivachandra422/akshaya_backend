"""
Resume Ally — Final Production-Grade Resume Intelligence Ally for Akshaya
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
        Analyze raw resume text and extract core insights.
        """
        summary_prompt = (
            "Analyze this resume and extract:
            - Candidate name
            - Years of experience
            - Technical skills
            - Soft skills
            - Gaps or weaknesses
            Return structured JSON only."
        )

        messages = [
            {"role": "system", "content": "You are a resume evaluation expert."},
            {"role": "user", "content": f"Resume:\n\n{text}\n\n{summary_prompt}"}
        ]

        try:
            result = query_openai(messages)
            insight = json.loads(result)
        except Exception as e:
            insight = {"error": str(e), "raw": result if 'result' in locals() else None}

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Analyzed resume and extracted structured summary.",
            "insight": insight
        })

        return insight

    def score(self, text: str) -> dict:
        """
        Score the resume for clarity, relevance, alignment, and ATS compliance.
        """
        score_prompt = (
            "Score this resume from 0 to 100 in:
            - Clarity
            - Role alignment
            - ATS friendliness
            - Technical relevance
            Return only JSON."
        )

        messages = [
            {"role": "system", "content": "You are an ATS optimization expert."},
            {"role": "user", "content": f"Resume:\n\n{text}\n\n{score_prompt}"}
        ]

        try:
            result = query_openai(messages)
            scores = json.loads(result)
        except Exception as e:
            scores = {"error": str(e), "raw": result if 'result' in locals() else None}

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Scored resume on critical hiring metrics.",
            "insight": scores
        })

        return scores

    def improve(self, text: str) -> str:
        """
        Return an improved version of the resume text.
        """
        improve_prompt = (
            "Rewrite and improve this resume to be more concise, professional, and optimized for ATS."
        )

        messages = [
            {"role": "system", "content": "You are a resume writing AI."},
            {"role": "user", "content": f"{improve_prompt}\n\n{text}"}
        ]

        try:
            improved = query_openai(messages)
        except Exception as e:
            improved = f"Error improving resume: {e}"

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Improved resume output generated.",
            "insight": improved[:1000]
        })

        return improved