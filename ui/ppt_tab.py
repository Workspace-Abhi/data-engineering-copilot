"""PPT story interface tab."""
import streamlit as st
from config.logging_config import get_logger
from agents.ppt_agent import get_ppt_agent

logger = get_logger("ppt_tab")

def render_ppt_tab():
    """Render the presentation agent interface."""
    st.header("📑 Presentation Agent")
    st.caption("Executive presentation storylines and structure")

    ppt_agent = get_ppt_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "🎯 Create Storyline", "📊 Generate Slide", "📝 Executive Summary"],
        horizontal=True
    )

    if sub_tab == "💬 Chat":
        query = st.text_area("Ask about presentations:", 
                            placeholder="How should I structure this presentation? What's the best storyline for...", 
                            height=100)
        if st.button("Submit", type="primary", key="ppt_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    response = ppt_agent.process(query)
                    st.markdown(response)

    elif sub_tab == "🎯 Create Storyline":
        topic = st.text_input("Presentation Topic", "Data Platform Modernization")
        audience = st.selectbox("Audience", ["executive", "technical", "mixed", "client"])
        duration = st.slider("Duration (minutes)", 10, 120, 30)

        key_points = st.text_area("Key Points to Cover (one per line)", 
                                  "Current platform limitations\nProposed architecture\nImplementation timeline\nExpected ROI\nRisk mitigation", 
                                  height=100)

        if st.button("Create Storyline", type="primary"):
            points = [p.strip() for p in key_points.split("\n") if p.strip()]
            with st.spinner("Creating storyline..."):
                result = ppt_agent.create_storyline(topic, audience, points, duration)
                st.markdown(result["storyline"])
                st.info(f"Duration: {result['duration']} minutes | Audience: {result['audience']}")

    elif sub_tab == "📊 Generate Slide":
        slide_title = st.text_input("Slide Title", "Current Architecture Challenges")
        slide_type = st.selectbox("Slide Type", ["content", "data", "comparison", "conclusion", "title"])
        context = st.text_area("Context/Background", "Our current data platform has scalability issues...", height=100)
        data_points = st.text_area("Data Points (one per line)", "50% increase in data volume\n2 hour ETL delays\n3 system outages this quarter", height=100)

        if st.button("Generate Slide", type="primary"):
            points = [p.strip() for p in data_points.split("\n") if p.strip()]
            with st.spinner("Generating slide..."):
                result = ppt_agent.generate_slide_content(slide_title, slide_type, context, points)
                st.markdown(result["content"])

    elif sub_tab == "📝 Executive Summary":
        content = st.text_area("Full Content", 
                              placeholder="Paste your detailed content, analysis, or report here...", 
                              height=300)
        max_length = st.slider("Max Words", 100, 500, 250)

        if st.button("Generate Summary", type="primary"):
            if content:
                with st.spinner("Summarizing..."):
                    summary = ppt_agent.executive_summary(content, max_length)
                    st.markdown("## Executive Summary")
                    st.markdown(summary)
                    st.download_button("Download Summary", summary, file_name="executive_summary.md")
