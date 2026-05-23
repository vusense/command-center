"""Framework selection logic from 04-framework-selection.md decision tree."""

from typing import Literal

Alignment = Literal["FULL", "PARTIAL", "NONE"]
RevType = Literal["I", "II", "III", "IV"]

FRAMEWORKS = (
    "5-Minute Rule",
    "ICE",
    "RAPID",
    "ASOFF",
    "Weighted Matrix",
    "STOP",
    "Alignment Resolution",
)


def recommend_framework(
    rev_type: RevType,
    risk_score: int,
    alignment: Alignment,
    flags: dict | None = None,
) -> tuple[str, list[str]]:
    """
    Return (primary_framework, alternatives).
    flags may include: values_based, time_critical, high_complexity
    """
    flags = flags or {}

    if flags.get("values_based"):
        return "STOP", ["Alignment Resolution"]

    if rev_type == "IV":
        return "STOP", ["Weighted Matrix"]

    if rev_type == "I":
        if flags.get("time_critical"):
            return "RAPID", ["5-Minute Rule"]
        return "5-Minute Rule", ["ICE"]

    if rev_type == "II":
        if risk_score <= 8:
            return "ICE", ["ASOFF"]
        if risk_score <= 12:
            return "ASOFF", ["Weighted Matrix"]
        return "Weighted Matrix", ["ASOFF"]

    # Type III — branch on alignment
    if alignment == "FULL":
        if flags.get("time_critical"):
            return "RAPID", ["5-Minute Rule"]
        if flags.get("high_complexity"):
            return "Weighted Matrix", ["RAPID"]
        return "RAPID", ["Weighted Matrix"]
    if alignment == "PARTIAL":
        return "ASOFF", ["STOP"]
    return "Alignment Resolution", ["STOP"]
