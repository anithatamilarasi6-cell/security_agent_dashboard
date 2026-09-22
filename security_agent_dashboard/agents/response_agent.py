"""
Response Recommendation Agent
-------------------------------
Maps a risk level to a SAFE, non-destructive recommended action.
This agent NEVER performs a real system change — it only produces a
recommendation string. Any higher-impact action is explicitly flagged
as requiring human approval, and the "approval" in this prototype only
updates in-memory demo state, never a real system.
"""

from dataclasses import dataclass


@dataclass
class ResponsePlan:
    action: str
    description: str
    requires_human_approval: bool


class ResponseAgent:
    """Prototype agent: recommends a safe next action based on risk level."""

    name = "Response Recommendation Agent"

    ACTIONS = {
        "LOW": ResponsePlan(
            action="Monitor",
            description="Continue passive monitoring. No user-facing action needed.",
            requires_human_approval=False,
        ),
        "MEDIUM": ResponsePlan(
            action="Request Verification",
            description="Prompt the (simulated) user to re-verify identity via MFA or a security question.",
            requires_human_approval=False,
        ),
        "HIGH": ResponsePlan(
            action="Temporarily Restrict Account (Simulated)",
            description="Recommend a temporary hold on the simulated account pending investigation.",
            requires_human_approval=True,
        ),
        "CRITICAL": ResponsePlan(
            action="Escalate to Security Team",
            description="Escalate the simulated incident to the human security team for immediate review.",
            requires_human_approval=True,
        ),
    }

    def recommend(self, risk_level: str) -> ResponsePlan:
        return self.ACTIONS.get(risk_level, self.ACTIONS["LOW"])
