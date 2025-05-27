"""
Capsule Graph — Final Sovereign Capsule Link Visualizer and Memory Network Ally
"""

from datetime import datetime
from collections import defaultdict
from modules.capsule_memory import list_capsules, store_capsule

class CapsuleGraph:
    def __init__(self):
        self.name = "capsule_graph"

    def generate_graph(self, limit: int = 30) -> dict:
        """
        Analyze recent capsules and form a symbolic graph based on source and reflection type.
        Returns a node-link graph structure.
        """
        capsules = list_capsules(limit=limit)
        graph = {"nodes": [], "links": []}
        node_map = {}
        node_index = 0

        for cap in capsules:
            source = cap.get("source", "unknown")
            reflection = cap.get("reflection", "unspecified")
            insight = cap.get("insight", "")
            key = f"{source}-{reflection[:40]}"

            if key not in node_map:
                node_map[key] = node_index
                graph["nodes"].append({"id": node_index, "label": reflection[:60], "source": source})
                node_index += 1

            # link to previous
            if len(graph["nodes"]) > 1:
                graph["links"].append({
                    "from": node_map.get(key, 0),
                    "to": node_map.get(list(node_map.keys())[-2], 0),
                    "type": "temporal"
                })

        store_capsule({
            "timestamp": datetime.utcnow().isoformat(),
            "source": self.name,
            "reflection": "Generated symbolic memory graph from capsule history.",
            "insight": graph
        })

        return graph