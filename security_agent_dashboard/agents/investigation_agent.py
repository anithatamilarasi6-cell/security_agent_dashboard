"""
Investigation Agent
--------------------
Given a set of flagged event IDs from the Detection Agent, this agent
correlates related events (same user / same IP), builds a chronological
timeline, and produces a structured evidence bundle for downstream agents.
"""

from dataclasses import dataclass, field
from typing import List, Dict

import pandas as pd


@dataclass
class InvestigationReport:
    username: str
    ip_address: str
    location: str
    timeline: List[Dict] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    failed_attempt_count: int = 0
    unusual_location: bool = False
    unusual_time: bool = False


class InvestigationAgent:
    """Prototype agent: correlates and summarizes evidence around a flagged incident."""

    name = "Investigation Agent"

    KNOWN_SAFE_LOCATIONS = {"Chennai, IN", "Coimbatore, IN", "Bengaluru, IN", "Mumbai, IN"}

    def investigate(self, events_df: pd.DataFrame, matched_event_ids: List[str]) -> InvestigationReport:
        subset = events_df[events_df["event_id"].isin(matched_event_ids)].sort_values("timestamp")
        if subset.empty:
            return InvestigationReport(username="unknown", ip_address="unknown", location="unknown")

        username = subset["username"].mode().iat[0]
        ip_address = subset["ip_address"].mode().iat[0]
        location = subset["location"].mode().iat[0]

        timeline = []
        for _, row in subset.iterrows():
            timeline.append(
                {
                    "time": row["timestamp"].strftime("%H:%M:%S"),
                    "event": row["event_type"],
                    "success": bool(row["success"]),
                }
            )

        evidence = []
        failed_count = int((subset["success"] == False).sum())  # noqa: E712
        if failed_count:
            evidence.append(f"{failed_count} failed authentication attempts correlated to the same account/IP pair")

        unusual_location = location not in self.KNOWN_SAFE_LOCATIONS
        if unusual_location:
            evidence.append(f"Login originated from an atypical location: {location}")

        unusual_time = any(row["hour_of_day"] in range(0, 6) for _, row in subset.iterrows())
        if unusual_time:
            evidence.append("Activity occurred outside normal working hours (00:00–06:00)")

        if subset["suspicious_indicator"].any():
            evidence.append(f"Source IP {ip_address} matches a synthetic watchlist indicator")

        return InvestigationReport(
            username=username,
            ip_address=ip_address,
            location=location,
            timeline=timeline,
            evidence=evidence,
            failed_attempt_count=failed_count,
            unusual_location=unusual_location,
            unusual_time=unusual_time,
        )
