"""Hybrid Search service combining RAG vector, TF-IDF keyword, and Graph relationships."""
from typing import Dict, List, Optional
from services.rag_service import get_rag_service
from services.knowledge_graph import get_knowledge_graph

class HybridSearchService:
    """Combines vector embeddings, keyword relevance, and relationship maps search results."""

    def __init__(self):
        self.rag_service = get_rag_service()
        self.knowledge_graph = get_knowledge_graph()

    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Perform unified search returning documents and contextual lineage info."""
        # 1. Pull merged vector & keyword search results
        results = self.rag_service.search(query, k=k)

        # 2. Extract potential entity tokens to pull graph lineage
        for result in results:
            content_lower = result["content"].lower()
            impact_tables = []
            
            # Simple keyword matching to trace graph node hits
            for node_id in self.knowledge_graph.nodes.keys():
                if node_id in content_lower:
                    downstream = self.knowledge_graph.find_downstream_dependencies(node_id)
                    if downstream:
                        impact_tables.append({
                            "entity": node_id,
                            "downstream_impact": downstream
                        })
            
            if impact_tables:
                result["metadata"]["graph_lineage_impact"] = impact_tables

        return results


def get_hybrid_search() -> HybridSearchService:
    """Get Hybrid Search instance."""
    return HybridSearchService()
