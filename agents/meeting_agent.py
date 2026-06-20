"""Meeting Agent for transcript analysis and action item extraction."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("meeting_agent")

class MeetingAgent:
    """Specialized agent for meeting transcript analysis."""

    SYSTEM_PROMPT = """You are an expert Meeting Facilitator and Project Coordinator. You specialize in:
- Transcript summarization and key point extraction
- Action item identification with owners and deadlines
- Decision tracking and rationale documentation
- Risk and issue identification from discussions
- Follow-up task creation and prioritization
- Meeting effectiveness analysis
- Stakeholder concern identification
- Next meeting agenda suggestions

Always provide structured output with clear sections and actionable items."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a meeting-related query."""
        rag_context = self.rag_service.get_context(query, k=3)

        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with structured meeting analysis."""

        response = self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

        return response

    def analyze_transcript(self, transcript: str) -> Dict:
        """Analyze a meeting transcript comprehensively."""
        analysis_prompt = f"""Analyze the following meeting transcript and provide:

## 1. Meeting Summary
- Key topics discussed
- Main decisions made
- Overall meeting objective

## 2. Action Items
For each action item, specify:
- Description
- Owner (if mentioned)
- Deadline (if mentioned)
- Priority (High/Medium/Low)
- Status (Open/Closed)

## 3. Decisions Made
- Decision description
- Rationale/justification
- Impact assessment

## 4. Risks & Issues Identified
- Description
- Severity
- Mitigation approach

## 5. Follow-up Items
- Topics for next meeting
- Information needed
- Stakeholders to engage

## 6. Sentiment Analysis
- Overall meeting tone
- Areas of consensus
- Points of contention

Transcript:
{transcript}
"""

        response = self.llm_service.generate(analysis_prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.3)
        return {"analysis": response}

    def extract_action_items(self, transcript: str) -> List[Dict]:
        """Extract only action items from a transcript."""
        action_prompt = f"""Extract all action items from the following meeting transcript.
Return ONLY a JSON array of action items with these fields:
- description: string
- owner: string (or "Unassigned")
- deadline: string (or "Not specified")
- priority: string (High/Medium/Low)

Transcript:
{transcript}

Response format: JSON array only, no markdown formatting."""

        response = self.llm_service.generate(action_prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.2)

        # Try to parse JSON, fallback to text
        try:
            import json
            action_items = json.loads(response)
            return action_items if isinstance(action_items, list) else []
        except:
            return [{"description": response, "owner": "Unassigned", "deadline": "Not specified", "priority": "Medium"}]

    def generate_meeting_minutes(self, transcript: str, meeting_title: str = "Team Meeting",
                                  attendees: List[str] = None, date: str = None) -> str:
        """Generate formal meeting minutes."""
        attendees_str = ", ".join(attendees) if attendees else "Not specified"

        minutes_prompt = f"""Generate formal meeting minutes from the following transcript.

Meeting Details:
- Title: {meeting_title}
- Date: {date or "Not specified"}
- Attendees: {attendees_str}

Format:
# Meeting Minutes: {meeting_title}

## Attendees
{attendees_str}

## Agenda Items
[List main topics]

## Discussion Summary
[For each topic, summarize key points]

## Decisions Made
[Numbered list]

## Action Items
[Table format with Owner, Task, Due Date]

## Next Steps
[What happens next]

## Next Meeting
[Date/time if mentioned]

Transcript:
{transcript}
"""

        response = self.llm_service.generate(minutes_prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.3)
        return response


def get_meeting_agent() -> MeetingAgent:
    """Get Meeting agent instance."""
    return MeetingAgent()
