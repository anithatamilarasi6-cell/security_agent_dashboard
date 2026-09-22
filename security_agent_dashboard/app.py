"""
Autonomous AI Security Agents — Research Prototype Dashboard
==============================================================
A research prototype demonstrating a proposed multi-agent cybersecurity
monitoring framework. ALL data is synthetic. ALL "AI agent" reasoning is
implemented as deterministic, transparent Python logic (no external LLM
API calls, no real network access, no real system changes).

Run with:  streamlit run app.py
"""

import time
from datetime import datetime

import pandas as pd
import streamlit as st

from data.synthetic_data import build_dataset, generate_suspicious_login_incident
from agents.detection_agent import DetectionAgent
from agents.investigation_agent import InvestigationAgent
from agents.threat_intel_agent import ThreatIntelAgent
from agents.risk_assessment_agent import RiskAssessmentAgent
from agents.response_agent import ResponseAgent
from utils.styling import DARK_THEME_CSS

st.set_page_config(
    page_title="Multi-Agent SOC Dashboard (Prototype)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
def init_state():
    if "events_df" not in st.session_state:
        st.session_state.events_df = build_dataset(include_incident=True)
    if "incident_history" not in st.session_state:
        st.session_state.incident_history = []
    if "current_result" not in st.session_state:
        st.session_state.current_result = None
    if "approval_status" not in st.session_state:
        st.session_state.approval_status = "Pending"
    if "workflow_progress" not in st.session_state:
        st.session_state.workflow_progress = []


init_state()

detection_agent = DetectionAgent()
investigation_agent = InvestigationAgent()
threat_intel_agent = ThreatIntelAgent()
risk_agent = RiskAssessmentAgent()
response_agent = ResponseAgent()


# ---------------------------------------------------------------------------
# Core pipeline runner
# ---------------------------------------------------------------------------
def run_pipeline(events_df, animate=False, status_container=None):
    """Runs the full agent pipeline once. If animate=True, updates a
    status_container step-by-step (used by both 'Run Investigation' and
    'Run Demo Incident')."""
    steps = []

    def log_step(label):
        steps.append(label)
        if status_container is not None:
            render_steps(status_container, steps)
            time.sleep(0.6)

    log_step("Detection Agent ✓")
    detection = detection_agent.scan(events_df)

    if not detection.is_suspicious:
        return {
            "detection": detection,
            "investigation": None,
            "threat_intel": None,
            "risk": None,
            "response": None,
        }

    log_step("Investigation Agent ✓")
    investigation = investigation_agent.investigate(events_df, detection.matched_event_ids)

    log_step("Threat Intelligence Agent ✓")
    threat_intel = threat_intel_agent.analyze(investigation)

    log_step("Risk Assessment Agent ✓")
    risk = risk_agent.calculate(investigation, threat_intel)

    log_step("Response Agent ✓")
    response = response_agent.recommend(risk.level)

    return {
        "detection": detection,
        "investigation": investigation,
        "threat_intel": threat_intel,
        "risk": risk,
        "response": response,
    }


def render_steps(container, steps):
    all_labels = [
        "Detection Agent ✓",
        "Investigation Agent ✓",
        "Threat Intelligence Agent ✓",
        "Risk Assessment Agent ✓",
        "Response Agent ✓",
    ]
    html = ""
    for label in all_labels:
        if label in steps:
            html += f'<div class="agent-step done">✅ {label}</div>'
        else:
            html += f'<div class="agent-step pending">⏳ {label.replace(" ✓","")}</div>'
    container.markdown(html, unsafe_allow_html=True)


def risk_badge(level):
    return f'<span class="risk-badge risk-{level}">{level}</span>'


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ Prototype Controls")
    st.caption("Research prototype — synthetic data only")

    if st.button("🔎 Run Investigation", use_container_width=True):
        status_box = st.empty()
        result = run_pipeline(st.session_state.events_df, animate=True, status_container=status_box)
        st.session_state.current_result = result
        st.session_state.approval_status = "Pending"
        if result["risk"] is not None:
            st.session_state.incident_history.append(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": result["investigation"].username,
                    "risk_score": result["risk"].score,
                    "risk_level": result["risk"].level,
                    "action": result["response"].action,
                    "status": "Pending",
                }
            )

    st.markdown("---")
    st.markdown("### 🎬 Demo Mode")
    st.caption("60–90 second competition demo")
    if st.button("▶️ Run Demo Incident", use_container_width=True, type="primary"):
        st.session_state.events_df = build_dataset(include_incident=True)
        status_box = st.empty()
        demo_narration = st.empty()

        narration_steps = [
            "1️⃣ Suspicious event detected...",
            "2️⃣ Investigation begins...",
            "3️⃣ Evidence correlated...",
            "4️⃣ Threat intelligence checked...",
            "5️⃣ Risk calculated...",
            "6️⃣ Response recommended...",
            "7️⃣ Human approval requested...",
        ]
        for n in narration_steps:
            demo_narration.info(n)
            time.sleep(0.5)

        result = run_pipeline(st.session_state.events_df, animate=True, status_container=status_box)
        st.session_state.current_result = result
        st.session_state.approval_status = "Pending"
        if result["risk"] is not None:
            st.session_state.incident_history.append(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": result["investigation"].username,
                    "risk_score": result["risk"].score,
                    "risk_level": result["risk"].level,
                    "action": result["response"].action,
                    "status": "Pending",
                }
            )
        demo_narration.success("✅ INCIDENT INVESTIGATION COMPLETE")

    st.markdown("---")
    if st.button("🔄 Reset Demo", use_container_width=True):
        st.session_state.events_df = build_dataset(include_incident=True)
        st.session_state.incident_history = []
        st.session_state.current_result = None
        st.session_state.approval_status = "Pending"
        st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ Synthetic Event Generator")
    if st.button("➕ Inject New Suspicious Event", use_container_width=True):
        new_rows = generate_suspicious_login_incident()
        new_df = pd.DataFrame(new_rows)
        st.session_state.events_df = pd.concat(
            [st.session_state.events_df, new_df], ignore_index=True
        ).sort_values("timestamp").reset_index(drop=True)
        st.success("New synthetic suspicious event batch injected.")


# ---------------------------------------------------------------------------
# Header / disclaimer banner
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="soc-banner">
        <h2 style="margin-bottom:4px;">🛡️ Autonomous AI Security Agents — SOC Dashboard</h2>
        <p style="color:#8b98a9; margin:0;">
        A research prototype demonstrating a proposed multi-agent cybersecurity monitoring
        framework. All data is synthetic; all agent reasoning is deterministic Python logic
        clearly labeled as a prototype workflow — not a production security system.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Top metrics
# ---------------------------------------------------------------------------
events_df = st.session_state.events_df
total_events = len(events_df)
suspicious_events = int(events_df["suspicious_indicator"].sum())
active_incidents = len([h for h in st.session_state.incident_history if h["status"] == "Pending"])
current_risk_level = (
    st.session_state.current_result["risk"].level
    if st.session_state.current_result and st.session_state.current_result["risk"]
    else "—"
)

col1, col2, col3, col4 = st.columns(4)
for col, label, value in zip(
    [col1, col2, col3, col4],
    ["Total Security Events", "Detected Suspicious Events", "Active Incidents", "Current Risk Level"],
    [total_events, suspicious_events, active_incidents, current_risk_level],
):
    col.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------------------------
# Main layout: Incident detail (left) + Agent activity / timeline (right)
# ---------------------------------------------------------------------------
left, right = st.columns([1.4, 1])

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 🚨 Current Incident Details")

    result = st.session_state.current_result
    if result is None:
        st.info("No investigation run yet. Click **Run Investigation** or **Run Demo Incident** in the sidebar.")
    elif result["risk"] is None:
        st.success("Detection Agent found no suspicious activity in the current event set.")
    else:
        inv = result["investigation"]
        risk = result["risk"]
        resp = result["response"]

        st.markdown(f"**User:** `{inv.username}`  &nbsp;&nbsp; **Source IP:** `{inv.ip_address}`")
        st.markdown(f"**Location:** {inv.location}")
        st.markdown(
            f"**Risk Score:** {risk.score}/100 &nbsp;&nbsp; {risk_badge(risk.level)}",
            unsafe_allow_html=True,
        )

        st.markdown("**Recommended Action:**")
        st.markdown(f"### {resp.action}")
        st.caption(resp.description)

        if resp.requires_human_approval:
            st.warning("⚠️ This response requires human approval before any (simulated) action is taken.")
            approve_col, deny_col = st.columns(2)
            with approve_col:
                if st.button("✅ Approve Response", use_container_width=True):
                    st.session_state.approval_status = "Approved"
                    if st.session_state.incident_history:
                        st.session_state.incident_history[-1]["status"] = "Approved"
            with deny_col:
                if st.button("❌ Deny / Escalate Manually", use_container_width=True):
                    st.session_state.approval_status = "Denied"
                    if st.session_state.incident_history:
                        st.session_state.incident_history[-1]["status"] = "Denied"

            status = st.session_state.approval_status
            if status == "Approved":
                st.success("Human approval recorded. (Simulated action logged — no real system was changed.)")
            elif status == "Denied":
                st.error("Response denied by human reviewer. Incident remains open for manual handling.")
            else:
                st.info("Awaiting human approval.")
        else:
            st.info("Low-impact action — no human approval required for this recommendation.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Evidence panel
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 🔍 Evidence Discovered")
    if result and result["investigation"]:
        for ev in result["investigation"].evidence:
            st.markdown(f'<div class="evidence-item">• {ev}</div>', unsafe_allow_html=True)
    else:
        st.caption("No evidence to display yet.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Threat intel panel
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 🌐 Threat Intelligence Analysis")
    if result and result["threat_intel"]:
        ti = result["threat_intel"]
        st.markdown(f"**IP Reputation:** {ti.ip_reputation}")
        st.markdown(f"**Attack Pattern:** {ti.attack_pattern_label}")
        st.markdown(f"**Confidence:** {ti.confidence}")
        for note in ti.notes:
            st.caption(note)
    else:
        st.caption("No threat intelligence data yet.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Risk score breakdown
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 📊 Risk Score Breakdown (Prototype Formula)")
    if result and result["risk"]:
        breakdown_df = pd.DataFrame(result["risk"].breakdown)
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
        st.caption("Prototype/demo scoring weights — not an empirically validated risk model.")
    else:
        st.caption("No risk score calculated yet.")
    st.markdown("</div>", unsafe_allow_html=True)


with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 🤖 Agent Activity")
    if st.session_state.current_result:
        completed = []
        r = st.session_state.current_result
        if r["detection"] is not None:
            completed.append("Detection Agent ✓")
        if r["investigation"] is not None:
            completed.append("Investigation Agent ✓")
        if r["threat_intel"] is not None:
            completed.append("Threat Intelligence Agent ✓")
        if r["risk"] is not None:
            completed.append("Risk Assessment Agent ✓")
        if r["response"] is not None:
            completed.append("Response Agent ✓")
        render_steps(st, completed)
    else:
        st.caption("Agents are idle. Run an investigation to see step-by-step activity.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 🕒 Investigation Timeline")
    if result and result["investigation"] and result["investigation"].timeline:
        for item in result["investigation"].timeline:
            icon = "✅" if item["success"] else "❌"
            st.markdown(
                f'<div class="timeline-item"><span class="timeline-time">{item["time"]}</span>'
                f'{icon} {item["event"].replace("_"," ").title()}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("No timeline events yet.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 📁 Incident History")
    if st.session_state.incident_history:
        hist_df = pd.DataFrame(st.session_state.incident_history)
        st.dataframe(hist_df, use_container_width=True, hide_index=True)
    else:
        st.caption("No incidents recorded yet this session.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 📈 Event Volume (Synthetic)")
    hourly_counts = events_df.groupby(events_df["timestamp"].dt.floor("30min")).size()
    st.bar_chart(hourly_counts)
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="disclaimer-box">
    ⚠️ <b>Research Integrity Notice:</b> This is a research prototype demonstrating a proposed
    multi-agent cybersecurity monitoring framework. It is <b>not</b> a production-ready autonomous
    cybersecurity system. All events, indicators, and scores shown are synthetic/demo data and do
    not represent real-world detection rates, response times, or accuracy figures.
    </div>
    """,
    unsafe_allow_html=True,
)
