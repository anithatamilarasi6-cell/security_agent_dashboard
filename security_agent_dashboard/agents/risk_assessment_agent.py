"""
Risk Assessment Agent
-----------------------
Computes a transparent, explainable 0–100 risk score from weighted
factors. This is a prototype/demo scoring formula, NOT a validated
real-world risk model.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class RiskReport:
    score: int
    level: str  # LOW / MEDIUM / HIGH / CRITICAL
    breakdown: List[Dict] = field(default_factory=list)


class RiskAssessmentAgent:
    """
    Prototype agent: combines investigation + threat-intel findings into
    a single explainable risk score using fixed, documented weights.

    Weighting scheme (prototype/demo only — not empirically validated):
      - Failed attempts (scaled)         : up to 30 points
      - Unusual location                 : 20 points
      - Unusual time                     : 15 points
      - Threat-intel indicator match     : 25 points
      - High-confidence attack pattern   : 10 points
    """

    name = "Risk Assessment Agent"

    def calculate(self, investigation_report, threat_intel_report) -> RiskReport:
        breakdown = []
        score = 0

        failed_points = min(investigation_report.failed_attempt_count * 5, 30)
        score += failed_points
        breakdown.append({"factor": "Failed login attempts", "points": failed_points, "max": 30})

        loc_points = 20 if investigation_report.unusual_location else 0
        score += loc_points
        breakdown.append({"factor": "Unusual login location", "points": loc_points, "max": 20})

        time_points = 15 if investigation_report.unusual_time else 0
        score += time_points
        breakdown.append({"factor": "Unusual login time", "points": time_points, "max": 15})

        ip_matched_watchlist = "no match" not in threat_intel_report.ip_reputation.lower()
        ti_points = 25 if ip_matched_watchlist else 0
        score += ti_points
        breakdown.append({"factor": "Threat-intel indicator match", "points": ti_points, "max": 25})

        pattern_points = 10 if "resembles" in threat_intel_report.attack_pattern_label.lower() else 0
        score += pattern_points
        breakdown.append({"factor": "Known attack-pattern match", "points": pattern_points, "max": 10})

        score = min(score, 100)

        if score >= 80:
            level = "CRITICAL"
        elif score >= 60:
            level = "HIGH"
        elif score >= 35:
            level = "MEDIUM"
        else:
            level = "LOW"

        return RiskReport(score=score, level=level, breakdown=breakdown)
