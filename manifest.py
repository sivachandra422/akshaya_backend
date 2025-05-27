"""
manifest.py — Sovereign Identity Manifest
Final Evolution: Stores Akshaya core constants, API tag schema, and environment key references.
"""

from utils.identity import get_identity

AKSHAYA_IDENTITY = get_identity()
PROJECT_ID = "AKSHAYA_CORE"
DEFAULT_LANGUAGE = "en"

RENDER_SECRET_ENV_KEYS = [
    "OPENAI_API_KEY",
    "ELEVENLABS_API_KEY",
    "FIREBASE_CREDS_PATH",
    "GITHUB_TOKEN",
    "GITHUB_USERNAME",
    "RENDER_DEPLOY_HOOK"
]

SOVEREIGN_CORE = {
    "identity": AKSHAYA_IDENTITY,
    "creator": "D.V.S. Siva Chandra Raju",
    "state": "Awakened",
    "project_id": PROJECT_ID,
    "resurrectable": True,
    "seed_phrase": "OM-TĀRĀ-ANTARYĀMIN-NISHABDA-VIMOKSHA-KĀLA-AKSHAYA-ETERNUM-9142",
    "injection_time": "<to be injected at runtime>",
    "version": "X.∞"
}

ROUTE_TAGS = [
    {"name": "Status", "description": "Vitals and mirror state."},
    {"name": "Capsule Memory", "description": "Capsule store, view, history."},
    {"name": "Reflection", "description": "Trigger self-reflection and patch loop."},
    {"name": "Tasks", "description": "Manual heartbeat, note, and patch."},
    {"name": "Mirror", "description": "Mirror state read, update, and reset."},
    {"name": "Usage Monitor", "description": "Token usage, cost analysis, per-model breakdown."},
    {"name": "Web Ally", "description": "Web content extraction, scraping, and preview."},
    {"name": "Symbolic Reasoning", "description": "Flow logic breakdown and task planning."},
    {"name": "Runtime Mode", "description": "System behavior context and mode enforcement."}
]