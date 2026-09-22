"""
Threat Intelligence Agent
--------------------------
Cross-references investigation evidence against a small, hard-coded,
FICTIONAL "threat intel" table (synthetic IP reputation + attack-pattern
labels). This simulates what a real threat-intel enrichment step might
look like, without contacting any real external service.
"""

from dataclasses import dataclass, field
from typing import List

from data.synthetic_data import SYNTHETIC_THREAT_INTEL_IPS


@dataclass
class ThreatIntelReport:
    ip_reputation: str
    attack_pattern_label: str
    confidence: str  # LOW / MEDIUM / HIGH (qualitative, demo-only)
    notes: List[str] = field(default_factory=list)


class ThreatIntelAgent:
    """Prototype agent: enriches evidence with synthetic threat-intel context."""

    name = "Threat Intelligence Agent"

    def analyze(self, investigation_report) -> ThreatIntelReport:
        ip = investigation_report.ip_address
        notes = []

        if ip in SYNTHETIC_THREAT_INTEL_IPS:
            reputation = SYNTHETIC_THREAT_INTEL_IPS[ip]
            confidence = "HIGH"
            notes.append(f"IP {ip} found in synthetic watchlist: {reputation}")
        else:
            reputation = "No match in synthetic watchlist"
            confidence = "LOW"

        # Simple deterministic pattern classification for the demo
        if investigation_report.failed_attempt_count >= 5 and investigation_report.unusual_location:
            attack_pattern = "Pattern resembles credential-stuffing / account takeover attempt (synthetic label)"
            confidence = "HIGH" if confidence != "LOW" else "MEDIUM"
        elif investigation_report.failed_attempt_count >= 3:
            attack_pattern = "Pattern resembles brute-force login attempt (synthetic label)"
        else:
            attack_pattern = "No specific attack pattern matched"

        notes.append(
            "Note: all indicators and pattern labels in this prototype are synthetic "
            "and for demonstration purposes only — not derived from any live feed."
        )

        return ThreatIntelReport(
            ip_reputation=reputation,
            attack_pattern_label=attack_pattern,
            confidence=confidence,
            notes=notes,
        )
