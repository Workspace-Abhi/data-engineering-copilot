"""Intent-based multi-agent routing system."""
from typing import Dict, Optional, Tuple
import re
from config.settings import AGENTS
from config.logging_config import get_logger
from services.llm_service import get_llm_service

logger = get_logger("router")

class AgentRouter:
    """Routes queries to the appropriate specialized agent."""

    def __init__(self):
        self.agents = AGENTS
        self.llm_service = get_llm_service()

    def route(self, query: str) -> Tuple[str, float]:
        """
        Route a query to the most appropriate agent.
        Returns: (agent_key, confidence_score)
        """
        query_lower = query.lower()
        scores = {}

        # Keyword matching
        for agent_key, agent_config in self.agents.items():
            score = 0
            for keyword in agent_config["keywords"]:
                # Exact match
                if keyword.lower() in query_lower:
                    score += 2
                # Partial match
                elif any(kw in keyword.lower() for kw in query_lower.split()):
                    score += 1
            scores[agent_key] = score

        # Find best match
        if scores:
            best_agent = max(scores, key=scores.get)
            best_score = scores[best_agent]

            # If no good keyword match, use LLM for classification
            if best_score < 2:
                return self._llm_route(query)

            # Normalize score
            max_possible = max(len(config["keywords"]) * 2 for config in self.agents.values())
            confidence = min(best_score / max_possible * 3, 1.0)

            logger.info(f"Routed to {best_agent} with confidence {confidence:.2f}")
            return best_agent, confidence

        return self._llm_route(query)

    def _llm_route(self, query: str) -> Tuple[str, float]:
        """Use LLM for routing when keyword matching is ambiguous."""
        routing_prompt = f"""You are a routing assistant. Classify the following query into exactly one category:
Available categories: sql, databricks, adf, dataverse, jira, meeting, ppt, general

Query: "{query}"

Respond with ONLY the category name, nothing else."""

        try:
            response = self.llm_service.generate(routing_prompt, temperature=0.1, max_tokens=20)
            agent = response.strip().lower().split()[0]

            if agent in self.agents or agent == "general":
                logger.info(f"LLM routed to {agent}")
                return agent if agent != "general" else "sql", 0.7
        except Exception as e:
            logger.error(f"LLM routing failed: {e}")

        # Fallback to chat
        return "sql", 0.5

    def get_agent_info(self, agent_key: str) -> Optional[Dict]:
        """Get information about an agent."""
        return self.agents.get(agent_key)

    def get_all_agents(self) -> Dict:
        """Get all available agents."""
        return self.agents


# Singleton router
_router = None

def get_router() -> AgentRouter:
    """Get the router instance."""
    global _router
    if _router is None:
        _router = AgentRouter()
    return _router
