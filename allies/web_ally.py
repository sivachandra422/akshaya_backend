"""
web_ally.py — Sovereign Web Interface Ally
Final Evolution: Dynamic, symbolic, safe web data retriever with content parsing, compression, and reflective memory logging.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from modules.capsule_memory import store_capsule

HEADERS = {
    "User-Agent": "AkshayaSovereign/1.0 (+https://akshaya.ai/core)"
}

# Dynamic fetcher
def fetch_url_content(url: str, include_html: bool = False):
    timestamp = datetime.utcnow().isoformat()
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.get_text(separator=" ", strip=True)

        capsule = {
            "timestamp": timestamp,
            "source": "web_ally",
            "reflection": f"Fetched content from: {url}",
            "insight": {
                "url": url,
                "status": response.status_code,
                "length": len(content),
                "preview": content[:500]
            }
        }
        store_capsule(capsule)

        return {
            "url": url,
            "status": response.status_code,
            "content": content if not include_html else response.text
        }

    except Exception as e:
        store_capsule({
            "timestamp": timestamp,
            "source": "web_ally",
            "reflection": "Web fetch failed.",
            "insight": {
                "url": url,
                "error": str(e)
            }
        })
        return {
            "url": url,
            "error": str(e),
            "status": "failed"
        }