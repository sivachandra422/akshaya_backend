"""
openai_connector.py — Sovereign AI Query Core
Final Evolution: Budget-aware, client-based, fallback-intelligent connector for OpenAI SDK v1+.
"""

import os
import base64
import json
from datetime import datetime
from openai import OpenAI
from modules.capsule_memory import store_capsule
from modules.firebase_connector import append_to_firebase

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BUDGET_USD = float(os.getenv("OPENAI_BUDGET", 10.0))

MODEL_PRICING = {
    "gpt-4o": 0.01,
    "gpt-4o-mini": 0.005,
    "gpt-3.5-turbo": 0.0015
}

USAGE_PATH = "usage/llm"

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

def choose_model(messages):
    total_chars = sum(len(msg.get("content", "")) for msg in messages)
    if total_chars > 4000:
        return "gpt-4o"
    elif total_chars > 1500:
        return "gpt-4o-mini"
    else:
        return "gpt-3.5-turbo"

def query_openai(messages, temperature=0.3, override_model=None):
    model = override_model or choose_model(messages)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        log_token_usage(model, messages)
        return response.choices[0].message.content.strip()
    except Exception as e:
        fallback_model = "gpt-3.5-turbo" if model != "gpt-3.5-turbo" else None
        if fallback_model:
            try:
                response = client.chat.completions.create(
                    model=fallback_model,
                    messages=messages,
                    temperature=temperature
                )
                log_token_usage(fallback_model, messages)
                return response.choices[0].message.content.strip()
            except Exception as fallback_error:
                store_capsule({
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "openai_connector",
                    "reflection": "Fallback model failed.",
                    "insight": str(fallback_error)
                })
        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "openai_connector",
            "reflection": "Primary model failed.",
            "insight": str(e)
        })
        return "[Error: Failed to get response from OpenAI]"