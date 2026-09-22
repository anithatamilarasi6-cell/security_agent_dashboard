"""
Detection Agent
---------------
Scans the synthetic event stream for patterns that look suspicious.
This is deterministic rule-based logic (clearly labeled as a prototype
stand-in for a real ML/LLM-driven detector).
"""

from dataclasses import dataclass, field
from typing import List

import pandas as pd

UNUSUAL_HOURS = set(range(0, 6))  # midnight–6am treated as unusual for this demo


@dataclass
class DetectionResult:
    is_suspicious: bool
    reasons: List[str] = field(default_factory=list)
    matched_event_ids: List[str] = field(default_factory=list)


class DetectionAgent:
    """
    Prototype agent: identifies suspicious login patterns using simple,
    transparent, deterministic rules over the synthetic event dataframe.
    """

    name = "Detection Agent"

    def scan(self, events_df: pd.DataFrame) -> DetectionResult:
        reasons = []
        matched_ids = []

        failed = events_df[events_df["success"] == False]  # noqa: E712
        if not failed.empty:
            # group failures by (username, ip) to find bursts
            grouped = failed.groupby(["username", "ip_address"]).size()
            bursts = grouped[grouped >= 3]
            if not bursts.empty:
                reasons.append(
                    f"Detected {int(bursts.max())} failed login attempts in a short window"
                )
                matched_ids += failed["event_id"].tolist()

        unusual_time = events_df[events_df["hour_of_day"].isin(UNUSUAL_HOURS)]
        if not unusual_time.empty:
            reasons.append("Login activity occurred during an unusual time window (00:00–06:00)")
            matched_ids += unusual_time["event_id"].tolist()

        flagged_ip = events_df[events_df["suspicious_indicator"] == True]  # noqa: E712
        if not flagged_ip.empty:
            reasons.append("Source IP matches a synthetic threat-intel indicator")
            matched_ids += flagged_ip["event_id"].tolist()

        is_suspicious = len(reasons) > 0
        matched_ids = sorted(set(matched_ids))
        return DetectionResult(is_suspicious=is_suspicious, reasons=reasons, matched_event_ids=matched_ids)
