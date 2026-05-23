"""Reversibility Type I–IV classification."""

from typing import Literal

RevType = Literal["I", "II", "III", "IV"]


def suggest_type(
    *,
    undo_within_30_days: bool,
    reversal_cost_usd: float,
    reversal_time_weeks: float,
    has_irreversible_commitments: bool,
) -> RevType:
    """Heuristic suggestion; executives may override with rationale."""
    if reversal_cost_usd > 1_000_000 or reversal_time_weeks > 12 or (
        has_irreversible_commitments and not undo_within_30_days
    ):
        return "IV"
    if reversal_cost_usd > 100_000 or reversal_time_weeks > 4:
        return "III"
    if reversal_cost_usd > 10_000 or reversal_time_weeks > 1 or not undo_within_30_days:
        return "II"
    return "I"
