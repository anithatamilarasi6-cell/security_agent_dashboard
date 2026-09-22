"""Shared CSS for the dark, professional SOC-style dashboard theme."""

DARK_THEME_CSS = """
<style>
:root {
    --bg-main: #0b0f14;
    --bg-panel: #121821;
    --bg-panel-alt: #161d29;
    --border-color: #232c3a;
    --text-main: #e6edf3;
    --text-dim: #8b98a9;
    --accent-blue: #3b9dff;
    --accent-green: #2ecc71;
    --accent-yellow: #f1c40f;
    --accent-orange: #ff9f43;
    --accent-red: #ff4d4f;
}

.stApp {
    background-color: var(--bg-main);
    color: var(--text-main);
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
}

h1, h2, h3, h4 {
    color: var(--text-main) !important;
    font-weight: 600 !important;
}

.soc-banner {
    background: linear-gradient(90deg, #0b0f14 0%, #121821 100%);
    border: 1px solid var(--border-color);
    border-left: 4px solid var(--accent-blue);
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 18px;
}

.metric-card {
    background: var(--bg-panel);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 16px 18px;
    text-align: left;
}
.metric-label {
    color: var(--text-dim);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-main);
}

.panel {
    background: var(--bg-panel);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 16px;
}
.panel h4 {
    margin-top: 0;
    color: var(--accent-blue) !important;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.risk-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
}
.risk-LOW { background: rgba(46,204,113,0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
.risk-MEDIUM { background: rgba(241,196,15,0.15); color: var(--accent-yellow); border: 1px solid var(--accent-yellow); }
.risk-HIGH { background: rgba(255,159,67,0.15); color: var(--accent-orange); border: 1px solid var(--accent-orange); }
.risk-CRITICAL { background: rgba(255,77,79,0.15); color: var(--accent-red); border: 1px solid var(--accent-red); }

.agent-step {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 6px;
    margin-bottom: 4px;
    background: var(--bg-panel-alt);
    border: 1px solid var(--border-color);
    font-size: 0.92rem;
}
.agent-step.done { border-left: 3px solid var(--accent-green); }
.agent-step.pending { border-left: 3px solid var(--border-color); color: var(--text-dim); }

.evidence-item {
    padding: 6px 0;
    border-bottom: 1px dashed var(--border-color);
    font-size: 0.9rem;
    color: var(--text-main);
}

.timeline-item {
    display: flex;
    gap: 12px;
    padding: 6px 0;
    font-size: 0.87rem;
    border-bottom: 1px solid var(--border-color);
}
.timeline-time { color: var(--accent-blue); font-family: monospace; min-width: 70px; }

.disclaimer-box {
    background: rgba(59,157,255,0.08);
    border: 1px solid var(--accent-blue);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: var(--text-dim);
    margin-top: 10px;
}

div[data-testid="stMetricValue"] {
    color: var(--text-main);
}
</style>
"""
