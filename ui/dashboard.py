"""Interactive Dashboard tab module."""
import streamlit as st
from config.settings import AGENTS, VERSION
from utils.helpers import check_ollama_status, get_system_info
from services.conversation_memory import get_memory
from services.rag_service import get_rag_service

def render_dashboard_tab():
    """Render the landing page interactive dashboard."""
    
    # Custom glowing animation and dashboard-specific CSS
    st.markdown("""
    <style>
        .hero-banner {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 27, 75, 0.8) 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            position: relative;
            overflow: hidden;
        }
        .hero-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
            pointer-events: none;
        }
        .dashboard-stat-card {
            background: rgba(15, 23, 42, 0.55);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .dashboard-stat-card:hover {
            transform: translateY(-3px);
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 8px 24px rgba(56, 189, 248, 0.15);
        }
        .stat-val {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 5px;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-label {
            color: #94a3b8;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .flow-node {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 12px 18px;
            text-align: center;
            font-weight: bold;
            font-size: 0.95rem;
            color: #f3f4f6;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            transition: all 0.2s ease;
        }
        .flow-node:hover {
            border-color: #38bdf8;
            background: rgba(30, 41, 59, 0.95);
            transform: scale(1.03);
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
        }
        .flow-node.active {
            background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%) !important;
            border-color: #818cf8 !important;
            box-shadow: 0 0 20px rgba(129, 140, 248, 0.4) !important;
        }
        .flow-arrow {
            text-align: center;
            font-size: 1.5rem;
            color: #64748b;
            align-self: center;
        }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero-banner">
        <h2 style='margin-top: 0; color: #f3f4f6;'>Welcome to the Data Engineering Copilot Hub ⚡</h2>
        <p style='color: #cbd5e1; font-size: 1.05rem; margin-bottom: 0;'>
            An advanced, multi-agent AI assistant to streamline end-to-end data analytics lifecycles. 
            Navigate between focused modules using the sidebar categories, or explore system metrics and interactive utilities below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Real-Time Statistics Check
    ollama_status = check_ollama_status()
    is_simulated = st.session_state.get("simulated_mode", True)
    
    # Calculate stats
    memory = get_memory()
    msg_count = len(memory.get_history())
    
    rag_service = get_rag_service()
    try:
        if hasattr(rag_service, "db") and rag_service.db is not None:
            # InMemoryCollection or ChromaDB fallback
            if hasattr(rag_service.db, "get"):
                kb_count = len(rag_service.db.get().get("ids", []))
            elif hasattr(rag_service.db, "collection"):
                kb_count = len(rag_service.db.collection)
            else:
                kb_count = 12 # Default mock sample count
        else:
            kb_count = 12
    except Exception:
        kb_count = 12

    # KPI Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        status_text = "Simulated (Mock)" if is_simulated else (ollama_status.get("models", ["Active"])[0] if ollama_status["status"] == "running" else "Offline")
        st.markdown(f"""
        <div class="dashboard-stat-card">
            <div class="stat-val" style="color: {'#fb7185' if status_text == 'Offline' else '#38bdf8'};">{status_text}</div>
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

    # Main Grid (Layout Flow Explorer & FinOps Calculator)
    col_flow, col_calc = st.columns([3, 2])

    with col_flow:
        st.subheader("🗺️ Interactive Data Lifecycle Flow")
        st.caption("Click a data stage below to inspect active agents, typical pipelines, and quick-start recommendations.")
        
        # Grid layout for flowchart
        flow_stages = ["📥 Source", "🔷 Ingest", "🔥 Raw Lake", "🧱 Warehouse", "🤖 Serve & ML"]
        
        # Interactive stage selection using a radio or selector
        selected_stage = st.radio(
            "Select Data Stage:",
            options=flow_stages,
            index=0,
            horizontal=True,
            key="selected_flow_stage"
        )
        
        st.write("")
        
        # Flow representation in markdown
        nodes_html = ""
        for stage in flow_stages:
            active_class = "active" if stage == selected_stage else ""
            nodes_html += f"<div class='flow-node {active_class}' style='display:inline-block; margin: 5px 10px;'>{stage}</div>"
            if stage != flow_stages[-1]:
                nodes_html += "<span class='flow-arrow'> ➜ </span>"
        
        st.markdown(f"<div style='text-align: center; margin-bottom: 25px;'>{nodes_html}</div>", unsafe_allow_html=True)

        # Stage details display
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
        
        # Inputs
        vol_gb = st.slider("Daily Ingest Volume (GB)", min_value=10, max_value=5000, value=250, step=10, key="finops_vol")
        ret_days = st.slider("Storage Retention (Days)", min_value=7, max_value=365, value=90, step=7, key="finops_ret")
        run_hrs = st.slider("Daily Cluster Runtime (Hrs)", min_value=1, max_value=24, value=4, step=1, key="finops_run")
        
        # Computations
        # Standard compute = volume * runtime * rate (e.g. $0.06/GB/hr)
        compute_cost_day = vol_gb * run_hrs * 0.005
        # Standard storage = volume * retention * rate (e.g. $0.0008/GB/day)
        storage_cost_month = vol_gb * ret_days * 0.0008
        
        # Total annual cost
        total_annual = (compute_cost_day * 365) + (storage_cost_month * 12)
        
        # Projected savings using Copilot optimization (FinOps compression/compaction policies ~35%)
        savings = total_annual * 0.35
        
        # Display cost summary cards
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-top: 15px;">
            <div style="font-size: 0.9rem; color: #94a3b8; font-weight: bold; margin-bottom: 8px;">ANNUAL OPERATIONAL COST PROJECTION</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #f3f4f6; margin-bottom: 12px;">${total_annual:,.2f} <span style="font-size: 0.9rem; font-weight: normal; color: #64748b;">/ year</span></div>
            <hr style="border-color: rgba(255,255,255,0.05); margin: 10px 0;"/>
            <div style="font-size: 0.9rem; color: #818cf8; font-weight: bold; margin-bottom: 5px;">⚡ ESTIMATED COPILOT SAVINGS (35%)</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #34d399;">${savings:,.2f} <span style="font-size: 0.9rem; font-weight: normal; color: #64748b;">/ year</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive progress metric indicator
        savings_ratio = (savings / 25000.0) if savings <= 25000.0 else 1.0
        st.write("")
        st.write("Savings Level Index:")
        st.progress(savings_ratio)
        st.caption("Based on automated lifecycle tiering and Z-Order compaction suggestions.")

    st.divider()

    # Quick Launch dropdown list
    st.subheader("🚀 Quick-Launch Agent Index")
    selected_agent = st.selectbox(
        "Choose an Agent to view specs:",
        options=list(AGENTS.keys()),
        format_func=lambda x: f"{AGENTS[x]['icon']} {AGENTS[x]['name']}",
        key="quick_launch_agent_select"
    )
    
    agent_info = AGENTS[selected_agent]
    st.markdown(f"""
    <div class="agent-card" style="border-left: 4px solid #818cf8; margin-bottom: 15px;">
        <h3>{agent_info['icon']} {agent_info['name']}</h3>
        <p>{agent_info['description']}</p>
        <small><b>Associated Keywords:</b> {", ".join(agent_info['keywords'])}</small>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Open Agent Page", type="primary", key="launch_agent_btn"):
        REVERSE_MAP = {
            "sql": ("💾 Models & Databases", "🗃️ SQL"),
            "databricks": ("🛠️ Orchestration & Pipelines", "🔥 Databricks"),
            "adf": ("🛠️ Orchestration & Pipelines", "🔷 ADF"),
            "dataverse": ("💾 Models & Databases", "📊 Dataverse"),
            "jira": ("👥 Team & Reporting", "🐛 Jira"),
            "meeting": ("👥 Team & Reporting", "📝 Meetings"),
            "ppt": ("👥 Team & Reporting", "📑 PPT"),
            "data_quality": ("🛡️ Quality & Governance", "⚡ Data Quality"),
            "dbt": ("💾 Models & Databases", "🧱 dbt"),
            "airflow": ("🛠️ Orchestration & Pipelines", "🌪️ Airflow"),
            "terraform": ("🛡️ Quality & Governance", "🛠️ Terraform IaC"),
            "governance": ("🛡️ Quality & Governance", "🛡️ Governance"),
            "cost": ("🛡️ Quality & Governance", "💰 Cost"),
            "migration": ("👥 Team & Reporting", "🚢 Migration"),
            "observability": ("🛡️ Quality & Governance", "👁️ Observability"),
            "catalog": ("💾 Models & Databases", "📇 Catalog"),
            "testing": ("🛡️ Quality & Governance", "🧪 Testing"),
            "code_review": ("🛡️ Quality & Governance", "🔍 Code Review"),
            "streaming": ("🛠️ Orchestration & Pipelines", "🌊 Streaming"),
            "mlops": ("💾 Models & Databases", "🤖 MLOps")
        }
        
        if selected_agent in REVERSE_MAP:
            cat, display_name = REVERSE_MAP[selected_agent]
            # Update session state to redirect navigation
            st.session_state["workspace_category_select"] = cat
            st.session_state["workspace_module_radio"] = display_name
            st.session_state["active_category"] = cat
            st.session_state["active_module_display"] = display_name
            st.session_state["active_module"] = selected_agent
            st.rerun()
