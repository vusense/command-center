"""Tests for framework selection and risk scoring."""

import pytest

from app.engine.framework_selector import recommend_framework
from app.engine.reversibility import suggest_type
from app.engine.risk import risk_category, sum_risk_scores


def test_low_risk_type_i():
    scores = dict(financial=1, timeline=1, team=1, customer=1, strategic=1)
    assert sum_risk_scores(scores) == 5
    assert risk_category(5) == "LOW"
    primary, alts = recommend_framework("I", 5, "FULL")
    assert primary == "5-Minute Rule"
    assert "ICE" in alts


def test_medium_risk_type_ii_asoff():
    scores = dict(financial=2, timeline=2, team=2, customer=1, strategic=2)
    total = sum_risk_scores(scores)
    assert total == 9
    assert risk_category(total) == "MEDIUM"
    primary, alts = recommend_framework("II", total, "PARTIAL")
    assert primary == "ASOFF"


def test_type_iv_stop():
    scores = dict(financial=4, timeline=3, team=3, customer=2, strategic=4)
    total = sum_risk_scores(scores)
    assert total == 16
    primary, _ = recommend_framework("IV", total, "FULL")
    assert primary == "STOP"


def test_type_iii_no_alignment():
    primary, alts = recommend_framework("III", 11, "NONE")
    assert primary == "Alignment Resolution"
    assert "STOP" in alts


def test_type_iii_full_rapid():
    primary, _ = recommend_framework("III", 10, "FULL")
    assert primary == "RAPID"


def test_values_based_stop():
    primary, alts = recommend_framework("I", 5, "FULL", {"values_based": True})
    assert primary == "STOP"
    assert "Alignment Resolution" in alts


def test_reversibility_suggest():
    assert suggest_type(
        undo_within_30_days=True,
        reversal_cost_usd=5000,
        reversal_time_weeks=0.5,
        has_irreversible_commitments=False,
    ) == "I"
    assert suggest_type(
        undo_within_30_days=False,
        reversal_cost_usd=150_000,
        reversal_time_weeks=8,
        has_irreversible_commitments=True,
    ) in ("III", "IV")
