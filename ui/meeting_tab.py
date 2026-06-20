"""Meeting notes interface tab."""
import streamlit as st
from config.logging_config import get_logger
from agents.meeting_agent import get_meeting_agent

logger = get_logger("meeting_tab")

def render_meeting_tab():
    """Render the meeting analysis interface."""
    st.header("📝 Meeting Agent")
    st.caption("Transcript analysis and action item extraction")

    meeting_agent = get_meeting_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "🔍 Full Analysis", "✅ Extract Action Items", "📄 Generate Minutes"],
        horizontal=True
    )

    if sub_tab == "💬 Chat":
        query = st.text_area("Ask about meetings:", 
                            placeholder="Summarize this meeting... What are the key decisions from...", 
                            height=100)
        if st.button("Submit", type="primary"):
            if query:
                with st.spinner("Analyzing..."):
                    response = meeting_agent.process(query)
                    st.markdown(response)

    elif sub_tab == "🔍 Full Analysis":
        transcript = st.text_area("Meeting Transcript", 
                                 placeholder="Paste your meeting transcript here...", 
                                 height=300)

        if st.button("Analyze", type="primary"):
            if transcript:
                with st.spinner("Analyzing transcript..."):
                    result = meeting_agent.analyze_transcript(transcript)
                    st.markdown(result["analysis"])

    elif sub_tab == "✅ Extract Action Items":
        transcript = st.text_area("Meeting Transcript", 
                                 placeholder="Paste your meeting transcript here...", 
                                 height=300)

        if st.button("Extract Action Items", type="primary"):
            if transcript:
                with st.spinner("Extracting..."):
                    action_items = meeting_agent.extract_action_items(transcript)
                    if isinstance(action_items, list):
                        for item in action_items:
                            with st.container():
                                cols = st.columns([3, 1, 1, 1])
                                cols[0].write(f"**{item.get('description', 'N/A')}**")
                                cols[1].caption(f"Owner: {item.get('owner', 'Unassigned')}")
                                cols[2].caption(f"Due: {item.get('deadline', 'Not specified')}")
                                priority = item.get('priority', 'Medium')
                                color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(priority, "⚪")
                                cols[3].caption(f"{color} {priority}")
                    else:
                        st.write(action_items)

    elif sub_tab == "📄 Generate Minutes":
        col1, col2 = st.columns(2)
        with col1:
            meeting_title = st.text_input("Meeting Title", "Sprint Planning")
            attendees = st.text_input("Attendees (comma-separated)", "John, Jane, Bob")
        with col2:
            meeting_date = st.date_input("Meeting Date")

        transcript = st.text_area("Meeting Transcript", 
                                 placeholder="Paste your meeting transcript here...", 
                                 height=250)

        if st.button("Generate Minutes", type="primary"):
            if transcript:
                with st.spinner("Generating minutes..."):
                    minutes = meeting_agent.generate_meeting_minutes(
                        transcript, 
                        meeting_title, 
                        attendees.split(",") if attendees else None,
                        str(meeting_date)
                    )
                    st.markdown(minutes)
                    st.download_button("Download Minutes", minutes, file_name=f"{meeting_title}_minutes.md")
