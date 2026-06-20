"""PPT story interface tab."""
import streamlit as st
from config.logging_config import get_logger
from agents.ppt_agent import get_ppt_agent

logger = get_logger("ppt_tab")

def render_slide_preview(title: str, slide_type: str, bullet_points: list):
    """Render a beautiful mock PowerPoint slide in HTML."""
    bullet_list_html = "".join([f"<li style='margin-bottom: 12px; font-size: 1.05rem;'>{point}</li>" for point in bullet_points])
    slide_html = f"""
    <div style="
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 12px;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5);
        padding: 35px;
        width: 100%;
        max-width: 800px;
        aspect-ratio: 16 / 9;
        color: #f3f4f6;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        position: relative;
        margin: 25px auto;
        overflow: hidden;
    ">
        <!-- Top bar/header -->
        <div style="border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 15px; margin-bottom: 22px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 1.7rem; font-weight: 800; background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</span>
            <span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">{slide_type} Slide</span>
        </div>
        
        <!-- Content Body -->
        <div style="height: calc(100% - 95px); overflow-y: auto; padding-right: 10px;">
            <ul style="padding-left: 20px; margin: 0; list-style-type: square; color: #cbd5e1; line-height: 1.6;">
                {bullet_list_html}
            </ul>
        </div>
        
        <!-- Slide Footer decoration -->
        <div style="position: absolute; bottom: 15px; left: 35px; right: 35px; font-size: 0.7rem; color: #64748b; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
            <span>🤖 Data Engineering Copilot Presentation Engine</span>
            <span style="font-weight: bold; color: #94a3b8;">Slide Preview</span>
        </div>
    </div>
    """
    st.markdown(slide_html, unsafe_allow_html=True)

def render_ppt_tab():
    """Render the presentation agent interface."""
    st.header("📑 Presentation Agent")
    st.caption("Executive presentation storylines and structure")

    ppt_agent = get_ppt_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "🎯 Create Storyline", "📊 Generate Slide", "📝 Executive Summary"],
        horizontal=True,
        key="ppt_operation_radio"
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

        if st.button("Create Storyline", type="primary", key="ppt_story_btn"):
            points = [p.strip() for p in key_points.split("\n") if p.strip()]
            with st.spinner("Creating storyline..."):
                result = ppt_agent.create_storyline(topic, audience, points, duration)
                st.markdown(result["storyline"])
                st.info(f"Duration: {result['duration']} minutes | Audience: {result['audience']}")

    elif sub_tab == "📊 Generate Slide":
        slide_title = st.text_input("Slide Title", "Current Architecture Challenges", key="ppt_slide_title")
        slide_type = st.selectbox("Slide Type", ["content", "data", "comparison", "conclusion", "title"], key="ppt_slide_type")
        context = st.text_area("Context/Background", "Our current data platform has scalability issues...", height=100, key="ppt_slide_ctx")
        data_points = st.text_area("Data Points (one per line)", "50% increase in data volume\n2 hour ETL delays\n3 system outages this quarter", height=100, key="ppt_slide_data")

        if st.button("Generate Slide", type="primary", key="ppt_slide_btn"):
            points = [p.strip() for p in data_points.split("\n") if p.strip()]
            with st.spinner("Generating slide..."):
                result = ppt_agent.generate_slide_content(slide_title, slide_type, context, points)
                
                # Render visual HTML slide preview
                st.subheader("🖼️ Visual Slide Deck Preview")
                render_slide_preview(slide_title, slide_type, points)
                st.divider()
                
                # Output text content
                st.subheader("📝 Generated Slide Content Details")
                st.markdown(result["content"])

    elif sub_tab == "📝 Executive Summary":
        content = st.text_area("Full Content", 
                               placeholder="Paste your detailed content, analysis, or report here...", 
                               height=300)
        max_length = st.slider("Max Words", 100, 500, 250)

        if st.button("Generate Summary", type="primary", key="ppt_summary_btn"):
            if content:
                with st.spinner("Summarizing..."):
                    summary = ppt_agent.executive_summary(content, max_length)
                    st.markdown("## Executive Summary")
                    st.markdown(summary)
                    st.download_button("Download Summary", summary, file_name="executive_summary.md", key="ppt_download_summary")
