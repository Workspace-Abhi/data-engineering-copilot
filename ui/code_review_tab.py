"""Code Review agent interface tab."""
import streamlit as st
from agents.code_review_agent import get_code_review_agent

def render_code_review_tab():
    st.header("🔍 Code Review Agent")
    st.caption("Review SQL, Python, or PySpark code snippets for anti-patterns and performance bottlenecks")

    review_agent = get_code_review_agent()

    chat_sub, paste_sub = st.tabs(["💬 Chat", "📋 Paste & Review Snippet"])

    with chat_sub:
        query = st.text_area("Ask about code best practices:",
                             placeholder="What are the main performance issues with using collect() in Spark?",
                             key="rev_chat_query",
                             height=100)
        if st.button("Submit Query", type="primary", key="rev_chat_submit"):
            if query:
                with st.spinner("Analyzing..."):
                    res = review_agent.process(query)
                    st.markdown(res)

    with paste_sub:
        st.subheader("Lint and Review Code Snippet")
        lang = st.selectbox("Code Language", ["sql", "python"], key="rev_lang")
        code = st.text_area("Paste Code Snippet", value="SELECT * FROM raw_users AS U JOIN transactions ON U.id = transactions.user_id", height=150, key="rev_code")
        
        if st.button("Review Snippet", type="primary", key="rev_btn"):
            res = review_agent.review_code_snippet(code, lang)
            st.markdown(f"#### Review Results ({res['language'].upper()})")
            
            for f in res["findings"]:
                severity_color = {
                    "Critical": "red",
                    "Warning": "orange",
                    "Info": "blue"
                }.get(f["severity"], "grey")
                
                st.markdown(f"""
                *   **Severity**: :{severity_color}[{f['severity']}]
                *   **Category**: `{f['category']}`
                *   **Description**: {f['description']}
                *   **Recommended Fix**: `{f['fix']}`
                """)
                st.divider()
            st.success("Review Completed!")
