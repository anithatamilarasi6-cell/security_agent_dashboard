# Autonomous AI Security Agents — Research Prototype

**A research prototype demonstrating a proposed multi-agent cybersecurity monitoring framework.**

> ⚠️ **Research Integrity Notice**
> This is a prototype for a research paper/symposium demonstration. It is **not** a
> production-ready autonomous cybersecurity system. It does not connect to any real
> network, does not scan or attack anything, and does not perform any real system
> changes. All events, IP addresses, "threat intelligence," and risk scores are
> **synthetic and fictional**, generated for demonstration purposes only. No metric
> shown (risk score, detection outcome, etc.) represents a real-world accuracy,
> detection-rate, or response-time figure — they are prototype/demo values only.

---

## 1. Project Folder Structure

```
security_agent_dashboard/
│
├── app.py                        # Main Streamlit dashboard application
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── agents/                        # One module per "AI agent" (deterministic logic)
│   ├── __init__.py
│   ├── detection_agent.py         # Detection Agent
│   ├── investigation_agent.py     # Investigation Agent
│   ├── threat_intel_agent.py      # Threat Intelligence Agent
│   ├── risk_assessment_agent.py   # Risk Assessment Agent
│   └── response_agent.py          # Response Recommendation Agent
│
├── data/
│   ├── synthetic_data.py          # Synthetic event generator (fake data only)
│   └── sample_events.csv          # A static sample synthetic dataset
│
└── utils/
    └── styling.py                 # Dark SOC-style CSS for the dashboard
```

---

## 2. Setup Instructions (Windows)

1. **Install Python 3.10+** from [python.org](https://www.python.org/downloads/) if not
   already installed. During installation, check **"Add Python to PATH."**

2. **Open Command Prompt (or PowerShell)** and navigate to the project folder:
   ```
   cd path\to\security_agent_dashboard
   ```

3. **(Recommended) Create a virtual environment:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## 3. Exact Command to Run the App

```
streamlit run app.py
```

Streamlit will open the dashboard automatically in your default browser
(typically at `http://localhost:8501`). If it doesn't open automatically,
copy the printed **Local URL** into your browser.

---

## 4. Explanation of Every Component

### `data/synthetic_data.py` — Synthetic Event Generator
Generates two kinds of fake login events:
- **Normal events**: everyday logins from known cities, at normal hours, always successful.
- **Suspicious incident**: a burst of failed logins from an unusual city, at an unusual
  hour (3 AM), from an IP address matched against a small **hard-coded, fictional**
  "threat intel" table (`SYNTHETIC_THREAT_INTEL_IPS`), followed by one final "successful"
  login — a simplified stand-in for an account-takeover pattern used purely to give the
  downstream agents something interesting to reason about.

### `agents/detection_agent.py` — Detection Agent
Scans the full synthetic event table for three deterministic red flags:
1. 3+ failed logins from the same user/IP in the dataset (a "burst").
2. Any login during the 00:00–06:00 window.
3. Any event whose `suspicious_indicator` flag is set (i.e., matched a fake watchlist IP).

If any of these fire, it flags the relevant event IDs as suspicious and hands them to the
Investigation Agent.

### `agents/investigation_agent.py` — Investigation Agent
Takes the flagged event IDs, pulls the full related event history for that
user/IP pair, and builds:
- A chronological **timeline** of what happened and when.
- A plain-English **evidence list** (e.g., "6 failed authentication attempts correlated to
  the same account/IP pair").
- Boolean flags for `unusual_location` and `unusual_time`, used later in risk scoring.

### `agents/threat_intel_agent.py` — Threat Intelligence Agent
Cross-references the investigated IP against the same fictional watchlist and applies
simple rule-based "attack pattern" labeling (e.g., "resembles credential-stuffing /
account takeover attempt"). This simulates what a real threat-intel enrichment step
might look like architecturally — it does **not** call any real threat-intel feed.

### `agents/risk_assessment_agent.py` — Risk Assessment Agent
Combines the investigation and threat-intel findings into a single **0–100 risk score**
using a fixed, fully transparent weighting scheme (see Section 5 below), then buckets
the score into LOW / MEDIUM / HIGH / CRITICAL.

### `agents/response_agent.py` — Response Recommendation Agent
Maps the risk level to one of four safe, non-destructive recommended actions
(Monitor → Request Verification → Temporarily Restrict Account (Simulated) → Escalate
to Security Team). HIGH and CRITICAL recommendations are flagged as
**requiring human approval**; the agent itself never performs any real action.

### Human Approval Layer (in `app.py`)
When a response requires approval, the dashboard shows **Approve** / **Deny** buttons.
Clicking them only updates in-memory session state (for the demo) — no real account,
system, or network is ever touched.

### `app.py` — Dashboard
Wires all five agents together into the pipeline, renders the SOC-style dark UI,
manages session state (current incident, incident history, approval status), and
implements the **Run Investigation**, **Run Demo Incident**, **Reset Demo**, and
**Inject New Suspicious Event** controls.

### `utils/styling.py`
Pure CSS for the dark, professional dashboard look (cards, badges, panels, timeline).

---

## 5. Explanation of the Risk-Scoring Formula

The Risk Assessment Agent computes a score out of 100 as the sum of five
independently-capped factors. **This is a prototype/demo formula for illustrating a
transparent, explainable scoring approach — it has not been empirically validated
against real attack data.**

| Factor                              | Points Awarded                          | Max Points |
|--------------------------------------|------------------------------------------|:----------:|
| Failed login attempts                 | `min(failed_attempts × 5, 30)`           | 30         |
| Unusual login location                | 20 if location is outside the known list | 20         |
| Unusual login time                    | 15 if login occurred 00:00–06:00         | 15         |
| Threat-intel indicator match           | 25 if the IP matched the synthetic watchlist | 25     |
| Known attack-pattern match             | 10 if a rule-based pattern label matched | 10         |

**Total is capped at 100.** Risk levels are then assigned as:

| Score Range | Level    |
|-------------|----------|
| 0–34        | LOW      |
| 35–59       | MEDIUM   |
| 60–79       | HIGH     |
| 80–100      | CRITICAL |

The dashboard's Risk Score Breakdown panel shows exactly how many points came from
each factor for full transparency/explainability, which is one of the framework's
design goals.

---

## 6. 60–90 Second Demo Instructions

1. Launch the app (`streamlit run app.py`).
2. In the sidebar, click **"▶️ Run Demo Incident."**
3. Narrate along with the on-screen steps as they animate:
   *"A suspicious login is detected... the Investigation Agent correlates the related
   failed attempts... Threat Intelligence checks the source IP against our watchlist...
   Risk Assessment calculates a transparent score... the Response Agent recommends an
   action..."*
4. Point out the **Risk Score Breakdown** table — emphasize that every point is explainable.
5. Point out the **Human Approval Required** banner and click **Approve** to show the
   human-in-the-loop control.
6. Finish by pointing at **"INCIDENT INVESTIGATION COMPLETE"** and the updated
   **Incident History** panel.
7. Optionally click **"🔄 Reset Demo"** to reset before a second run-through.

Total run time is roughly 60–90 seconds depending on narration pace.

---

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| `streamlit: command not found` | Activate your virtual environment (`venv\Scripts\activate`) or run `pip install -r requirements.txt` again. |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` and open that port instead. |
| Blank/white page in browser | Wait a few seconds for Streamlit to finish compiling; refresh the page. |
| `ModuleNotFoundError: pandas` or `streamlit` | Confirm you're inside the activated virtual environment, then re-run `pip install -r requirements.txt`. |
| Charts look empty after Reset Demo | Click "Run Investigation" or "Run Demo Incident" again — the reset clears the current incident, not the underlying synthetic dataset. |
| App looks unstyled (no dark theme) | Ensure `utils/styling.py` is present and `app.py` is run from inside the `security_agent_dashboard` folder so relative imports resolve. |

---

## 8. How This Prototype Supports the Research Paper

The paper argues for a **multi-agent architecture** for cyber-threat detection and
response, where specialized agents each own one stage of the investigative pipeline
(detection → investigation → intelligence enrichment → risk scoring → response
recommendation → human approval). This prototype operationalizes that architecture
in miniature:

- It demonstrates **separation of concerns** across independently testable agent
  modules, supporting the paper's claim that modular agent design improves
  maintainability and auditability over a monolithic detection script.
- It demonstrates **explainable risk scoring** — every point in the final score can be
  traced back to a specific, human-readable factor, supporting the paper's emphasis on
  transparency in AI-assisted security decisions.
- It demonstrates a **human-in-the-loop control point** for high-impact actions, directly
  supporting the paper's safety argument that autonomous agents should recommend, not
  unilaterally execute, high-impact responses.
- Because it runs entirely on deterministic logic and synthetic data, it lets the paper
  discuss the proposed **workflow and interaction pattern** between agents without making
  any claims about real-world detection accuracy — which the paper can appropriately
  reserve for future work with real datasets and a live LLM/ML backend.

---

## 9. Suggested Screenshots for a 7-Slide Presentation

1. **Title slide**: dashboard header banner with the framework name and research
   disclaimer visible.
2. **Slide 2 — Architecture Overview**: the sidebar controls plus the "Agent Activity"
   panel showing the five-agent pipeline.
3. **Slide 3 — Detection**: top metrics row (Total Events / Suspicious Events / Active
   Incidents) right after clicking "Run Demo Incident."
4. **Slide 4 — Investigation & Evidence**: the "Evidence Discovered" and "Investigation
   Timeline" panels populated after a run.
5. **Slide 5 — Threat Intelligence & Risk Scoring**: the "Threat Intelligence Analysis"
   panel plus the "Risk Score Breakdown" table.
6. **Slide 6 — Response & Human Approval**: the recommended action, the
   "Human Approval Required" warning, and the Approve/Deny buttons.
7. **Slide 7 — Incident History / Closing**: the "Incident History" table and the
   research-integrity disclaimer banner at the bottom of the dashboard.
