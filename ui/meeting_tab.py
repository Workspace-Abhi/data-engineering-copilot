"""Meeting notes interface tab."""
import streamlit as st
from config.logging_config import get_logger
from agents.meeting_agent import get_meeting_agent

logger = get_logger("meeting_tab")

def get_sample_transcript():
    return """[00:01] DataEngLead: Welcome team. Today we need to align on our Azure Data Platform migration sync.
[00:02] DevOpsEngineer: I've set up the ADLS Gen2 landing zones. We're using Parquet format for raw landing.
[00:03] DataEngLead: Excellent. Now for Bronze to Silver, we need a robust Slowly Changing Dimension (SCD) Type 2 pattern in Spark.
[00:05] BusinessAnalyst: Yes, historical tracking is critical for customer profiles. We must track field changes over time and keep active records flagged as is_current = true.
[00:07] DataEngLead: Got it. Also, let's make sure the ADF Copy Activities are metadata-driven. We should query the control database to retrieve old watermark values, pull max source dates, copy incremental data, and write back the new watermark.
[00:09] DevOpsEngineer: I'll handle key vault credentials and MSAL auth token configurations. I have a script that gets OAuth tokens via Python MSAL Client application.
[00:10] DataEngLead: Sounds good. Let's ensure that the alternate keys mapping for CRM ingestion into Dataverse CRM Web API is documented by the end of the week.
[00:11] BusinessAnalyst: I will map the source fields to Dataverse cr234_customer fields.
"""

def render_meeting_tab():
    """Render the meeting analysis interface."""
    st.header("📝 Meeting Agent")
    st.caption("Transcript analysis and action item extraction")

    meeting_agent = get_meeting_agent()

    sub_tab = st.radio(
        "Select Operation",
        ["💬 Chat", "🔍 Full Analysis", "✅ Extract Action Items", "📄 Generate Minutes"],
        horizontal=True,
        key="meeting_operation_radio"
    )

    if sub_tab == "💬 Chat":
        query = st.text_area("Ask about meetings:", 
                            placeholder="Summarize this meeting... What are the key decisions from...", 
                            height=100)
        if st.button("Submit", type="primary", key="meeting_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    response = meeting_agent.process(query)
                    st.markdown(response)

    else:
        # Load sample transcript helper
        transcript_key = f"meeting_transcript_{sub_tab.replace(' ', '_')}"
        saved_transcript = st.session_state.get("sample_transcript", "")
        
        # Show load sample button if empty
        if not saved_transcript:
            if st.button("⚡ Load Premium Sample Transcript (Migration Sync)", key=f"meeting_load_btn_{sub_tab.replace(' ', '_')}"):
                st.session_state["sample_transcript"] = get_sample_transcript()
                st.rerun()
        else:
            if st.button("🗑️ Clear Sample Transcript", key=f"meeting_clear_btn_{sub_tab.replace(' ', '_')}"):
                st.session_state["sample_transcript"] = ""
                st.rerun()

        if sub_tab == "🔍 Full Analysis":
            transcript = st.text_area("Meeting Transcript", 
                                     value=st.session_state.get("sample_transcript", ""),
                                     placeholder="Paste your meeting transcript here...", 
                                     height=300,
                                     key=transcript_key)

            if st.button("Analyze", type="primary", key="meeting_analyze_btn"):
                if transcript:
                    with st.spinner("Analyzing transcript..."):
                        result = meeting_agent.analyze_transcript(transcript)
                        st.markdown(result["analysis"])

        elif sub_tab == "✅ Extract Action Items":
            transcript = st.text_area("Meeting Transcript", 
                                     value=st.session_state.get("sample_transcript", ""),
                                     placeholder="Paste your meeting transcript here...", 
                                     height=300,
                                     key=transcript_key)

            if st.button("Extract Action Items", type="primary", key="meeting_action_btn"):
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
                meeting_title = st.text_input("Meeting Title", "Sprint Planning", key="meeting_title_in")
                attendees = st.text_input("Attendees (comma-separated)", "John, Jane, Bob", key="meeting_attendees_in")
            with col2:
                meeting_date = st.date_input("Meeting Date", key="meeting_date_in")

            transcript = st.text_area("Meeting Transcript", 
                                     value=st.session_state.get("sample_transcript", ""),
                                     placeholder="Paste your meeting transcript here...", 
                                     height=250,
                                     key=transcript_key)

            if st.button("Generate Minutes", type="primary", key="meeting_minutes_btn"):
                if transcript:
                    with st.spinner("Generating minutes..."):
                        minutes = meeting_agent.generate_meeting_minutes(
                            transcript, 
                            meeting_title, 
                            attendees.split(",") if attendees else None,
                            str(meeting_date)
                        )
                        st.markdown(minutes)
                        st.download_button("Download Minutes", minutes, file_name=f"{meeting_title}_minutes.md", key="meeting_download_minutes")
