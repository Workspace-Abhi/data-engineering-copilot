"""PPT Agent for executive presentation storylines and structure."""
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.llm_service import get_llm_service
from services.rag_service import get_rag_service

logger = get_logger("ppt_agent")

class PPTAgent:
    """Specialized agent for presentation creation and storyline development."""

    SYSTEM_PROMPT = """You are an expert Executive Presentation Designer and Storyteller. You specialize in:
- Executive summary creation and key message development
- Data-driven narrative construction
- Slide structure and flow optimization
- Visual recommendation for complex data
- Stakeholder-specific messaging
- Call-to-action formulation
- Presentation pacing and timing
- Q&A preparation and objection handling

Always provide structured storyline recommendations with clear narrative arcs.
Focus on business impact and actionable insights."""

    def __init__(self):
        self.llm_service = get_llm_service()
        self.rag_service = get_rag_service()

    def process(self, query: str, context: str = "") -> str:
        """Process a presentation-related query."""
        rag_context = self.rag_service.get_context(query, k=3)

        full_prompt = f"""{self.SYSTEM_PROMPT}

Context from knowledge base:
{rag_context}

User Query: {query}

Additional Context: {context}

Provide a comprehensive response with presentation structure and storyline recommendations."""

        response = self.llm_service.generate(
            full_prompt,
            system_prompt=self.SYSTEM_PROMPT,
            temperature=0.3
        )

        return response

    def create_storyline(self, topic: str, audience: str = "executive",
                         key_points: List[str] = None, duration: int = 30) -> Dict:
        """Create a presentation storyline."""
        key_points_str = "\n".join([f"- {kp}" for kp in key_points]) if key_points else "To be determined"

        storyline_prompt = f"""Create a compelling presentation storyline for the following topic.

Topic: {topic}
Audience: {audience}
Duration: {duration} minutes
Key Points to Cover:
{key_points_str}

Provide:

## 1. Narrative Arc
- Hook/Opening (what grabs attention)
- Problem/Opportunity statement
- Solution/Approach
- Evidence/Proof points
- Call to action

## 2. Slide-by-Slide Breakdown
For each slide provide:
- Slide title
- Key message (1 sentence)
- Content bullets (3-5 points)
- Visual recommendation (chart type, diagram, image)
- Speaker notes (2-3 sentences)

## 3. Storytelling Techniques
- Analogies to use
- Data points to emphasize
- Emotional hooks
- Transition phrases

## 4. Audience-Specific Messaging
- What {audience} cares about most
- Potential objections and responses
- Decision drivers to highlight

## 5. Q&A Preparation
- Expected questions
- Recommended responses
- Supporting data to have ready
"""

        response = self.llm_service.generate(storyline_prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.3)
        return {"storyline": response, "topic": topic, "audience": audience, "duration": duration}

    def generate_slide_content(self, slide_title: str, slide_type: str = "content",
                                context: str = "", data_points: List[str] = None) -> Dict:
        """Generate content for a specific slide."""
        data_str = "\n".join([f"- {dp}" for dp in data_points]) if data_points else ""

        slide_prompt = f"""Generate content for the following presentation slide.

Slide Title: {slide_title}
Slide Type: {slide_type} (title, content, data, comparison, conclusion)
Context: {context}
Data Points: {data_str}

Provide:
1. Slide title (refined)
2. Subtitle (if applicable)
3. Content structure (bullets, numbered, or narrative)
4. Visual recommendation
5. Speaker notes
6. Key takeaway (1 sentence)
"""

        response = self.llm_service.generate(slide_prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.3)
        return {"content": response, "title": slide_title, "type": slide_type}

    def executive_summary(self, content: str, max_length: int = 250) -> str:
        """Generate an executive summary."""
        summary_prompt = f"""Create a powerful executive summary (max {max_length} words) from the following content.

Requirements:
- Start with the key message/insight
- Include 3-5 bullet points of critical information
- End with a clear recommendation or next step
- Use executive language (concise, impactful, action-oriented)
- Focus on business outcomes and ROI

Content:
{content}
"""

        response = self.llm_service.generate(summary_prompt, system_prompt=self.SYSTEM_PROMPT, temperature=0.3)
        return response


def get_ppt_agent() -> PPTAgent:
    """Get PPT agent instance."""
    return PPTAgent()
