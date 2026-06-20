"""Jira Agent for issue grouping, workstreams, and remediation."""
from typing import Dict, List, Optional
import pandas as pd
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("jira_agent")

class JiraAgent:
    """Specialized agent for Jira analysis and planning."""

    SYSTEM_PROMPT = """You are an expert Agile Project Manager and Jira Administrator. You specialize in:
- Issue categorization and grouping
- Workstream identification and prioritization
- Remediation planning and sprint allocation
- Velocity tracking and capacity planning
- Epic/story breakdown and estimation
- Root cause analysis for recurring issues
- Team workload balancing
- Risk assessment and mitigation strategies

Always provide actionable insights with clear next steps and priority levels."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a Jira-related query."""
        rag_context = self.rag_service.get_context(query, k=3)

        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with actionable recommendations and structured plans."""

        response = self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

        return response

    def analyze_issues(self, issues_df: pd.DataFrame) -> Dict:
        """Analyze Jira issues and provide grouping."""
        if issues_df.empty:
            return {"error": "No issues provided"}

        # Prepare summary for LLM
        summary = f"""Analyze the following Jira issues and provide:
1. Issue grouping by theme/category
2. Workstream identification
3. Priority-based remediation plan
4. Sprint allocation recommendations
5. Risk assessment

Issues Summary:
Total Issues: {len(issues_df)}
Columns: {', '.join(issues_df.columns.tolist())}

Sample Issues:
{issues_df.head(10).to_string()}

Key Statistics:
- Issue Types: {issues_df.get('Issue Type', pd.Series()).value_counts().to_dict() if 'Issue Type' in issues_df.columns else 'N/A'}
- Priorities: {issues_df.get('Priority', pd.Series()).value_counts().to_dict() if 'Priority' in issues_df.columns else 'N/A'}
- Status: {issues_df.get('Status', pd.Series()).value_counts().to_dict() if 'Status' in issues_df.columns else 'N/A'}
"""

        response = self.llm_service.generate(summary, system_prompt=self.SYSTEM_PROMPT, temperature=0.3)
        return {"analysis": response, "issue_count": len(issues_df)}

    def generate_remediation_plan(self, issues_df: pd.DataFrame, team_capacity: int = 40) -> Dict:
        """Generate a structured remediation plan."""
        plan_prompt = f"""Create a detailed remediation plan for {len(issues_df)} issues with team capacity of {team_capacity} story points per sprint.

Issues:
{issues_df.to_string()}

Provide:
1. Sprint-by-sprint breakdown
2. Story point allocation per sprint
3. Dependency mapping
4. Risk mitigation strategies
5. Success metrics
"""

        response = self.llm_service.generate(plan_prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.3)
        return {"plan": response, "sprints": "See detailed plan", "capacity": team_capacity}

    def group_by_theme(self, issues_df: pd.DataFrame) -> Dict:
        """Group issues by common themes."""
        if "Summary" not in issues_df.columns:
            return {"error": "Summary column required for theme grouping"}

        summaries = "\n".join([f"- {s}" for s in issues_df["Summary"].tolist()])

        grouping_prompt = f"""Group the following {len(issues_df)} Jira issue summaries into logical themes/workstreams.
Provide:
1. Theme names and descriptions
2. Issues per theme
3. Recommended epic structure
4. Cross-theme dependencies

Issue Summaries:
{summaries}
"""

        response = self.llm_service.generate(grouping_prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.3)
        return {"grouping": response}


def get_jira_agent() -> JiraAgent:
    """Get Jira agent instance."""
    return JiraAgent()
