"""Knowledge Graph service using an in-memory relationship mapper simulating Neo4j."""
from typing import Dict, List, Set, Tuple, Optional
from config.logging_config import get_logger

logger = get_logger("knowledge_graph")

class KnowledgeGraphService:
    """Simulates a Neo4j Graph DB mapping entities (tables, pipelines, columns) and relationships."""

    def __init__(self):
        self.nodes = {}  # node_id -> {"label": label, "properties": properties}
        self.edges = []  # List of Tuple (src_id, tgt_id, rel_type)
        self._seed_default_graph()

    def _seed_default_graph(self):
        """Preseed the graph with standard dependencies for the copilot demo."""
        self.add_node("raw_customers", "Table", {"domain": "sales"})
        self.add_node("stg_customers", "Table", {"domain": "sales"})
        self.add_node("dim_customers", "Table", {"domain": "sales"})
        self.add_node("fact_sales", "Table", {"domain": "finance"})
        self.add_node("ingestion_pipeline", "Pipeline", {"owner": "data_eng"})
        
        self.add_relationship("raw_customers", "stg_customers", "depends_on")
        self.add_relationship("stg_customers", "dim_customers", "depends_on")
        self.add_relationship("dim_customers", "fact_sales", "depends_on")
        self.add_relationship("ingestion_pipeline", "raw_customers", "produces")

    def add_node(self, node_id: str, label: str, properties: Dict = None):
        """Add an entity node."""
        self.nodes[node_id] = {
            "label": label,
            "properties": properties or {}
        }

    def add_relationship(self, src_id: str, tgt_id: str, rel_type: str):
        """Add a directed typed edge/relationship."""
        if src_id in self.nodes and tgt_id in self.nodes:
            self.edges.append((src_id, tgt_id, rel_type))

    def find_downstream_dependencies(self, node_id: str) -> List[str]:
        """Traverse the graph downstream to see what breaks if a node is modified."""
        visited = set()
        queue = [node_id]
        impacted = []

        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                if current != node_id:
                    impacted.append(current)
                # Find all nodes that depend_on the current node
                for src, tgt, rel in self.edges:
                    if src == current and rel == "depends_on":
                        queue.append(tgt)
                        
        return impacted

    def query_relationships(self, node_id: str) -> List[Dict]:
        """Find immediate relationships of a node."""
        rels = []
        for src, tgt, rel in self.edges:
            if src == node_id or tgt == node_id:
                rels.append({
                    "source": src,
                    "target": tgt,
                    "relationship": rel
                })
        return rels


def get_knowledge_graph() -> KnowledgeGraphService:
    """Get Knowledge Graph instance."""
    return KnowledgeGraphService()
