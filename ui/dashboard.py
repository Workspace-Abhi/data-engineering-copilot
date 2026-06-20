"""Interactive Dashboard tab module."""
import streamlit as st
from config.settings import AGENTS, VERSION
from utils.helpers import check_ollama_status, get_system_info
from services.conversation_memory import get_memory
from services.rag_service import get_rag_service

def render_dashboard_tab():
    """Render the landing page interactive dashboard."""

    # Detect current theme from session state
    dark = st.session_state.get("dark_mode", True)

    # ── Theme-aware palette ──────────────────────────────────────────
    if dark:
        HERO_BG        = "linear-gradient(135deg, rgba(15,23,42,0.85) 0%, rgba(30,27,75,0.85) 100%)"
        HERO_BORDER    = "rgba(99,102,241,0.25)"
        HERO_TITLE     = "#f3f4f6"
        HERO_TEXT      = "#cbd5e1"
        CARD_BG        = "rgba(15,23,42,0.55)"
        CARD_BORDER    = "rgba(255,255,255,0.08)"
        CARD_HOVER_BD  = "rgba(56,189,248,0.4)"
        STAT_VAL_GRAD  = "linear-gradient(to right, #38bdf8, #818cf8)"
        STAT_LABEL_COL = "#94a3b8"
        FLOW_NODE_BG   = "rgba(30,41,59,0.75)"
        FLOW_NODE_BD   = "rgba(255,255,255,0.08)"
        FLOW_NODE_TEXT = "#f3f4f6"
        FLOW_ACTIVE_BG = "linear-gradient(135deg, #1e1b4b 0%, #311042 100%)"
        FLOW_ACTIVE_BD = "#818cf8"
        ARROW_COLOR    = "#64748b"
        FINOPS_BG      = "rgba(15,23,42,0.5)"
        FINOPS_BORDER  = "rgba(255,255,255,0.06)"
        FINOPS_LABEL   = "#94a3b8"
        FINOPS_COST_CL = "#f3f4f6"
        FINOPS_MUTED   = "#64748b"
        FINOPS_SAVE_CL = "#818cf8"
        FINOPS_AMT_CL  = "#34d399"
        DIVIDER_COL    = "rgba(255,255,255,0.06)"
        AGENT_LEFT_BD  = "#818cf8"
    else:
        HERO_BG        = "linear-gradient(135deg, rgba(219,234,254,0.95) 0%, rgba(237,233,254,0.95) 100%)"
        HERO_BORDER    = "rgba(99,102,241,0.2)"
        HERO_TITLE     = "#1e293b"
        HERO_TEXT      = "#334155"
        CARD_BG        = "rgba(255,255,255,0.85)"
        CARD_BORDER    = "rgba(0,0,0,0.09)"
        CARD_HOVER_BD  = "rgba(2,132,199,0.5)"
        STAT_VAL_GRAD  = "linear-gradient(to right, #0284c7, #4f46e5)"
        STAT_LABEL_COL = "#475569"
        FLOW_NODE_BG   = "rgba(248,250,252,0.95)"
        FLOW_NODE_BD   = "rgba(0,0,0,0.1)"
        FLOW_NODE_TEXT = "#1e293b"
        FLOW_ACTIVE_BG = "linear-gradient(135deg, #dbeafe 0%, #ede9fe 100%)"
        FLOW_ACTIVE_BD = "#4f46e5"
        ARROW_COLOR    = "#94a3b8"
        FINOPS_BG      = "rgba(248,250,252,0.9)"
        FINOPS_BORDER  = "rgba(0,0,0,0.08)"
        FINOPS_LABEL   = "#475569"
        FINOPS_COST_CL = "#1e293b"
        FINOPS_MUTED   = "#94a3b8"
        FINOPS_SAVE_CL = "#4f46e5"
        FINOPS_AMT_CL  = "#059669"
        DIVIDER_COL    = "rgba(0,0,0,0.08)"
        AGENT_LEFT_BD  = "#4f46e5"

    # ── Dashboard CSS (theme-aware) ───────────────────────────────────
    st.markdown(f"""
    <style>
        .hero-banner {{
            background: {HERO_BG};
            border: 1px solid {HERO_BORDER};
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px 0 rgba(0,0,0,0.12);
            position: relative;
            overflow: hidden;
        }}
        .hero-banner::before {{
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
            pointer-events: none;
        }}
        .dashboard-stat-card {{
            background: {CARD_BG};
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid {CARD_BORDER};
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }}
        .dashboard-stat-card:hover {{
            transform: translateY(-3px);
            border-color: {CARD_HOVER_BD};
            box-shadow: 0 8px 24px rgba(56,189,248,0.12);
        }}
        .stat-val {{
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 5px;
            background: {STAT_VAL_GRAD};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .stat-label {{
            color: {STAT_LABEL_COL};
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .flow-node {{
            background: {FLOW_NODE_BG};
            border: 1px solid {FLOW_NODE_BD};
            border-radius: 10px;
            padding: 12px 18px;
            text-align: center;
            font-weight: bold;
            font-size: 0.95rem;
            color: {FLOW_NODE_TEXT};
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            transition: all 0.2s ease;
        }}
        .flow-node:hover {{
            border-color: {CARD_HOVER_BD};
            transform: scale(1.03);
        }}
        .flow-node.active {{
            background: {FLOW_ACTIVE_BG} !important;
            border-color: {FLOW_ACTIVE_BD} !important;
            color: {FLOW_NODE_TEXT} !important;
            box-shadow: 0 0 16px rgba(99,102,241,0.25) !important;
        }}
        .flow-arrow {{
            text-align: center;
            font-size: 1.4rem;
            color: {ARROW_COLOR};
            align-self: center;
        }}
    </style>
    """, unsafe_allow_html=True)

    # ── Hero Banner ──────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-banner">
        <h2 style='margin-top: 0; color: {HERO_TITLE};'>Welcome to the Data Engineering Copilot Hub ⚡</h2>
        <p style='color: {HERO_TEXT}; font-size: 1.05rem; margin-bottom: 0;'>
            An advanced, multi-agent AI assistant to streamline end-to-end data analytics lifecycles.
            Navigate between focused modules using the sidebar categories, or explore system metrics and interactive utilities below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Real-Time Stats ───────────────────────────────────────────────
    ollama_status = check_ollama_status()
    is_simulated = st.session_state.get("simulated_mode", True)

    memory = get_memory()
    msg_count = len(memory.get_history())

    rag_service = get_rag_service()
    try:
        if hasattr(rag_service, "db") and rag_service.db is not None:
            if hasattr(rag_service.db, "get"):
                kb_count = len(rag_service.db.get().get("ids", []))
            elif hasattr(rag_service.db, "collection"):
                kb_count = len(rag_service.db.collection)
            else:
                kb_count = 12
        else:
            kb_count = 12
    except Exception:
        kb_count = 12

    # ── KPI Cards ────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        status_text = "Simulated (Mock)" if is_simulated else (
            ollama_status.get("models", ["Active"])[0]
            if ollama_status["status"] == "running" else "Offline"
        )
        offline_color = "#fb7185" if not dark else "#fb7185"
        online_color  = "#0284c7" if not dark else "#38bdf8"
        val_color = offline_color if status_text == "Offline" else online_color
        st.markdown(f"""
        <div class="dashboard-stat-card">
            <div class="stat-val" style="background: none; -webkit-text-fill-color: {val_color};">{status_text}</div>
            <div class="stat-label">LLM Engine</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="dashboard-stat-card">
            <div class="stat-val">{kb_count} Docs</div>
            <div class="stat-label">Knowledge Base</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="dashboard-stat-card">
            <div class="stat-val">{msg_count} Msgs</div>
            <div class="stat-label">Session Memory</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="dashboard-stat-card">
            <div class="stat-val">{len(AGENTS)} Agents</div>
            <div class="stat-label">Active Modules</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ── Main Grid ─────────────────────────────────────────────────────
    col_flow, col_calc = st.columns([3, 2])

    with col_flow:
        st.subheader("🗺️ Interactive Data Lifecycle Flow")
        st.caption("Click a data stage below to inspect active agents, typical pipelines, and quick-start recommendations.")

        flow_stages = ["📥 Source", "🔷 Ingest", "🔥 Raw Lake", "🧱 Warehouse", "🤖 Serve & ML"]

        selected_stage = st.radio(
            "Select Data Stage:",
            options=flow_stages,
            index=0,
            horizontal=True,
            key="selected_flow_stage"
        )

        st.write("")

        nodes_html = ""
        for stage in flow_stages:
            active_class = "active" if stage == selected_stage else ""
            nodes_html += f"<div class='flow-node {active_class}' style='display:inline-block; margin: 5px 10px;'>{stage}</div>"
            if stage != flow_stages[-1]:
                nodes_html += "<span class='flow-arrow'> ➜ </span>"

        st.markdown(f"<div style='text-align: center; margin-bottom: 25px;'>{nodes_html}</div>", unsafe_allow_html=True)

        st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
        if selected_stage == "📥 Source":
            st.markdown("### 📥 Source Data Layer")
            st.write("Contains operational source systems, API hooks, catalog databases, and documents.")
            st.markdown("- **Relevant Agents**: Governance Agent, Data Catalog Agent, Jira Agent")
            st.markdown("- **Common Actions**: Ingestion schema cataloging, PII detection, documentation AST parsing.")
            st.code("""
# Source Connection Verification
curl -I https://api.source-service.internal/v1/health
            """, language="bash")
        elif selected_stage == "🔷 Ingest":
            st.markdown("### 🔷 Ingestion Layer")
            st.write("Responsible for ETL scheduling, pipeline triggers, file sensors, and incremental copies.")
            st.markdown("- **Relevant Agents**: ADF Agent, Airflow Agent, Streaming Agent")
            st.markdown("- **Common Actions**: Watermark updates, TaskGroup definitions, Spark Structured Streaming triggers.")
            st.code("""
# Incremental ADF Copy trigger expression
@utcnow()
            """, language="json")
        elif selected_stage == "🔥 Raw Lake":
            st.markdown("### 🔥 Raw Lake Layer (Bronze)")
            st.write("Uncleaned, high-throughput storage tier. Ingests raw files directly without transformation.")
            st.markdown("- **Relevant Agents**: Databricks Agent, Terraform IaC Agent, Cost Agent")
            st.markdown("- **Common Actions**: Delta table creation, lifecycle cold-tier policy, compute cluster sizing.")
            st.code("""
# Terraform raw S3 container definition
resource "aws_s3_bucket" "bronze" {
  bucket = "lake-bronze-storage"
}
            """, language="hcl")
        elif selected_stage == "🧱 Warehouse":
            st.markdown("### 🧱 Cleaned Warehouse Layer (Silver)")
            st.write("Transformations, deduplications, relational staging, and modular schema validation.")
            st.markdown("- **Relevant Agents**: SQL Agent, dbt Agent, Data Quality Agent, Testing Agent")
            st.markdown("- **Common Actions**: SCD Type 2 merge logic, Great Expectations validation suite, dbt snapshot staging.")
            st.code("""
-- dbt snapshot template
{% snapshot orders_snapshot %}
  {{ config(target_schema='snapshots', unique_key='id', strategy='check', check_cols=['status']) }}
  select * from {{ ref('orders') }}
{% endsnapshot %}
            """, language="sql")
        elif selected_stage == "🤖 Serve & ML":
            st.markdown("### 🤖 Serve & Machine Learning Layer (Gold)")
            st.write("Analytical aggregations, statistical drift detection, MLOps feature stores, and executive PPT reporting.")
            st.markdown("- **Relevant Agents**: MLOps Data Agent, PPT Agent, Observability Agent, Code Review Agent")
            st.markdown("- **Common Actions**: Feast feature view definition, Prometheus alerting rules, drift distribution mapping.")
            st.code("""
# MLOps statistical drift check
import scipy.stats as stats
drift_stat, p_value = stats.ks_2samp(ref_data, curr_data)
            """, language="python")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_calc:
        st.subheader("💰 Interactive FinOps Calculator")
        st.caption("Estimate data storage and pipeline compute savings dynamically based on your workloads.")

        vol_gb   = st.slider("Daily Ingest Volume (GB)",     min_value=10,  max_value=5000, value=250, step=10,  key="finops_vol")
        ret_days = st.slider("Storage Retention (Days)",     min_value=7,   max_value=365,  value=90,  step=7,   key="finops_ret")
        run_hrs  = st.slider("Daily Cluster Runtime (Hrs)",  min_value=1,   max_value=24,   value=4,   step=1,   key="finops_run")

        compute_cost_day   = vol_gb * run_hrs * 0.005
        storage_cost_month = vol_gb * ret_days * 0.0008
        total_annual       = (compute_cost_day * 365) + (storage_cost_month * 12)
        savings            = total_annual * 0.35

        st.markdown(f"""
        <div style="background: {FINOPS_BG}; border: 1px solid {FINOPS_BORDER};
                    padding: 18px; border-radius: 12px; margin-top: 15px;">
            <div style="font-size: 0.85rem; color: {FINOPS_LABEL}; font-weight: 700;
                        letter-spacing: 0.06em; margin-bottom: 8px;">
                ANNUAL OPERATIONAL COST PROJECTION
            </div>
            <div style="font-size: 1.9rem; font-weight: 800; color: {FINOPS_COST_CL}; margin-bottom: 10px;">
                ${total_annual:,.2f}
                <span style="font-size: 0.9rem; font-weight: 400; color: {FINOPS_MUTED};">/ year</span>
            </div>
            <hr style="border-color: {DIVIDER_COL}; margin: 10px 0;"/>
            <div style="font-size: 0.85rem; color: {FINOPS_SAVE_CL}; font-weight: 700; margin-bottom: 5px;">
                ⚡ ESTIMATED COPILOT SAVINGS (35%)
            </div>
            <div style="font-size: 1.5rem; font-weight: 800; color: {FINOPS_AMT_CL};">
                ${savings:,.2f}
                <span style="font-size: 0.9rem; font-weight: 400; color: {FINOPS_MUTED};">/ year</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        savings_ratio = min(savings / 25000.0, 1.0)
        st.write("")
        st.write("Savings Level Index:")
        st.progress(savings_ratio)
        st.caption("Based on automated lifecycle tiering and Z-Order compaction suggestions.")

    st.divider()

    # ── Quick Launch ──────────────────────────────────────────────────
    st.subheader("🚀 Quick-Launch Agent Index")
    selected_agent = st.selectbox(
        "Choose an Agent to view specs:",
        options=list(AGENTS.keys()),
        format_func=lambda x: f"{AGENTS[x]['icon']} {AGENTS[x]['name']}",
        key="quick_launch_agent_select"
    )

    agent_info = AGENTS[selected_agent]
    st.markdown(f"""
    <div class="agent-card" style="border-left: 4px solid {AGENT_LEFT_BD}; margin-bottom: 15px;">
        <h3>{agent_info['icon']} {agent_info['name']}</h3>
        <p>{agent_info['description']}</p>
        <small><b>Associated Keywords:</b> {", ".join(agent_info['keywords'])}</small>
    </div>
    """, unsafe_allow_html=True)


