"""Risk score calculation per decision-framework state gathering."""

from typing import Literal

RiskCategory = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

RISK_DOMAINS = (
    "financial",
    "timeline",
    "team",
    "customer",
    "strategic",
)


def sum_risk_scores(scores: dict[str, int]) -> int:
    for key in RISK_DOMAINS:
        if key not in scores:
            raise ValueError(f"Missing risk domain: {key}")
        val = scores[key]
        if not 1 <= val <= 4:
            raise ValueError(f"{key} score must be 1-4, got {val}")
    return sum(scores[k] for k in RISK_DOMAINS)


def risk_category(total: int) -> RiskCategory:
    if total <= 8:
        return "LOW"
    if total <= 12:
        return "MEDIUM"
    if total <= 16:
        return "HIGH"
    return "CRITICAL"
