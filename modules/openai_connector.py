"""
openai_connector.py — Sovereign AI Query Core
Final Evolution: Intelligent fallback, critical handling, model routing, and live billing integration.
"""

import os
import base64
import json
from datetime import datetime, timedelta
import requests
from openai import OpenAI
from modules.capsule_memory import store_capsule
from modules.firebase_connector import append_to_firebase

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BUDGET_USD = float(os.getenv("OPENAI_BUDGET", 10.0))
FORCE_USE_4O = os.getenv("FORCE_USE_4O", "false").lower() == "true"

MODEL_PRICING = {
    "gpt-4o-2024-08-06": 0.01,
    "gpt-4o-mini-2024-07-18": 0.002,
    "gpt-3.5-turbo": 0.0015
}

USAGE_PATH = "usage/llm"

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18")
FALLBACK_MODEL = "gpt-4o-2024-08-06"


def fetch_actual_spend(days_back=7):
    try:
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days_back)
        url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
        headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}
        res = requests.get(url, headers=headers)
        data = res.json()
        total_cents = data.get("total_usage", 0)
        return round(total_cents / 100, 4)  # USD
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "openai_connector",
            "reflection": "Failed to fetch OpenAI spend.",
            "insight": str(e)
        })
        return 0.0


def estimate_cost(messages, model):
    total_chars = sum(len(msg.get("content", "")) for msg in messages)
    token_estimate = total_chars / 4
    return (token_estimate / 1000) * MODEL_PRICING.get(model, 0.01)


def log_token_usage(model, messages):
    try:
        cost = estimate_cost(messages, model)
        append_to_firebase(USAGE_PATH, {
            "timestamp": datetime.utcnow().isoformat(),
            "model": model,
            "cost": cost
        })
    except Exception as e:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "openai_connector",
            "reflection": "Token logging failed.",
            "insight": str(e)
        })


def choose_model(messages, critical=False):
    if FORCE_USE_4O or critical:
        return FALLBACK_MODEL
    return DEFAULT_MODEL


def query_openai(messages, temperature=0.3, override_model=None, critical=False):
    current_spend = fetch_actual_spend()
    if current_spend >= BUDGET_USD:
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "openai_connector",
            "reflection": "Budget exceeded — blocking OpenAI call.",
            "insight": f"${current_spend} used out of ${BUDGET_USD}"
        })
        return "[Blocked: Budget cap exceeded]"

    model = override_model or choose_model(messages, critical)
    attempt = 0

    while attempt < 2:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            log_token_usage(model, messages)
            return response.choices[0].message.content.strip()
        except Exception as e:
            attempt += 1
            if model != FALLBACK_MODEL and (critical or attempt == 2):
                model = FALLBACK_MODEL
                continue
            elif model == FALLBACK_MODEL:
                store_capsule({
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "openai_connector",
                    "reflection": "GPT-4o fallback failed.",
                    "insight": str(e)
                })
                break
            else:
                store_capsule({
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "openai_connector",
                    "reflection": "GPT-mini model failed.",
                    "insight": str(e)
                })
                model = FALLBACK_MODEL
    return "[Error: Failed to get response from OpenAI]"