"""
capsule_graph.py — Symbolic Capsule Relationship Builder
Final Evolution: Constructs graph from memory capsules and logs symbolic insight.
"""

import json
from datetime import datetime
from modules.capsule_memory import store_capsule, list_capsules


def build_capsule_graph():
    try:
        capsules = list_capsules(limit=25)
        nodes = []
        links = []

        for i, cap in enumerate(capsules):
            node = {
                "id": i,
                "label": cap.get("source", f"capsule_{i}"),
                "timestamp": cap.get("timestamp", "")
            }
            nodes.append(node)

            if i > 0:
                links.append({
                    "source": i - 1,
                    "target": i,
                    "type": "reflection"
                })

        graph = {"nodes": nodes, "links": links}

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": "capsule_graph",
            "reflection": "Symbolic capsule network generated.",
            "insight": graph
        })

        return graph

    except Exception as e:
        print(f"[Capsule Graph Error] {e}")
        return {"error": str(e)}