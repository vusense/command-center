"""Decision Context Card — state assessment."""

import streamlit as st

from app.engine.framework_selector import recommend_framework
from app.engine.reversibility import suggest_type
from app.engine.risk import RISK_DOMAINS, risk_category, sum_risk_scores
from app.export import md_export
from app.storage import db
from app.ui_common import (
    ALIGNMENT_UI,
    alignment_to_engine,
    require_auth,
    sidebar_context,
)

st.set_page_config(page_title="Context Card", layout="wide")
actor = require_auth()
if not actor:
    st.stop()
sidebar_context(actor)

st.title("Gate 2 — Decision Context Card")

decisions = db.list_decisions()
if not decisions:
    st.warning("Start a decision from the Handoff page.")
    st.stop()

decision_id = st.selectbox(
    "Decision",
    [d["id"] for d in decisions],
    index=0
    if not st.session_state.get("decision_id")
    else ([d["id"] for d in decisions].index(st.session_state.decision_id) if st.session_state.decision_id in [d["id"] for d in decisions] else 0),
    format_func=lambda i: next(d["title"] for d in decisions if d["id"] == i),
)
st.session_state.decision_id = decision_id
decision = db.get_decision(decision_id)
ctx = db.get_context_card(decision_id) or {}

st.subheader("Gate 0")
exec_signoff = st.checkbox("Executive sign-off required", value=bool(decision.get("exec_signoff", 1)))
handoff_complete = st.checkbox("Problem Discovery handoff complete", value=bool(decision.get("handoff_complete", 0)))

st.subheader("Alignment")
prob_align = st.radio("Problem statement aligned?", ALIGNMENT_UI, index=ALIGNMENT_UI.index(ctx.get("problem_alignment", "YES")) if ctx.get("problem_alignment") in ALIGNMENT_UI else 0, horizontal=True)
metric_align = st.radio("Success metrics aligned?", ALIGNMENT_UI, index=ALIGNMENT_UI.index(ctx.get("metric_alignment", "YES")) if ctx.get("metric_alignment") in ALIGNMENT_UI else 0, horizontal=True)
values_vs = st.selectbox("Values vs tactical", ["TACTICAL", "VALUES", "BOTH"], index=["TACTICAL", "VALUES", "BOTH"].index(ctx.get("values_vs_tactical", "TACTICAL")) if ctx.get("values_vs_tactical") in ("TACTICAL", "VALUES", "BOTH") else 0)
align_notes = st.text_area("Alignment notes", value=ctx.get("alignment_notes", ""))

st.subheader("Risk assessment (1–4 each)")
risk_scores = ctx.get("risk_scores", {})
scores = {}
for domain in RISK_DOMAINS:
    prev = risk_scores.get(domain, {})
    c1, c2 = st.columns([1, 3])
    with c1:
        score_val = st.slider(domain.title(), 1, 4, int(prev.get("score", 2)), key=f"risk_{domain}")
    with c2:
        rationale = st.text_input(f"{domain} rationale", value=prev.get("rationale", ""), key=f"rat_{domain}")
    scores[domain] = {"score": score_val, "rationale": rationale}

total = sum_risk_scores({k: v["score"] for k, v in scores.items()})
cat = risk_category(total)
st.info(f"Risk score: **{total}/20** — {cat}")
mitigation = st.text_area("Risk mitigation", value=ctx.get("risk_mitigation", ""))

st.subheader("Reversibility")
undo = st.checkbox("Can undo within 30 days", value=bool(ctx.get("undo_30_days", 1)))
rev_cost = st.number_input("Reversal cost (USD)", min_value=0.0, value=float(ctx.get("reversal_cost", 0) or 0))
rev_weeks = st.number_input("Reversal time (weeks)", min_value=0.0, value=float(ctx.get("reversal_time_weeks", 0) or 0))
irrev = st.text_input("Irreversible commitments", value=ctx.get("irreversible_commitments", ""))
has_irrev = bool(irrev.strip())
suggested = suggest_type(
    undo_within_30_days=undo,
    reversal_cost_usd=rev_cost,
    reversal_time_weeks=rev_weeks,
    has_irreversible_commitments=has_irrev,
)
rev_type = st.selectbox("Reversibility type", ["I", "II", "III", "IV"], index=["I", "II", "III", "IV"].index(ctx.get("rev_type_override") or ctx.get("rev_type") or suggested))
st.caption(f"Suggested: Type {suggested}")

st.subheader("Framework flags")
values_based = st.checkbox("Values-based decision", value=ctx.get("flags", {}).get("values_based", False))
time_critical = st.checkbox("Time-critical", value=ctx.get("flags", {}).get("time_critical", False))
high_complexity = st.checkbox("High complexity", value=ctx.get("flags", {}).get("high_complexity", False))

align_engine = alignment_to_engine(metric_align if prob_align == metric_align else "PARTIAL")
if prob_align == "NO" or metric_align == "NO":
    align_engine = "NONE"
elif prob_align == "PARTIAL" or metric_align == "PARTIAL":
    align_engine = "PARTIAL"
else:
    align_engine = "FULL"

primary, alts = recommend_framework(
    rev_type,
    total,
    align_engine,
    {"values_based": values_based, "time_critical": time_critical, "high_complexity": high_complexity},
)
st.success(f"Recommended: **{primary}** — Alternatives: {', '.join(alts)}")

override = st.checkbox("Override framework", value=bool(ctx.get("framework_override")))
fw_choice = st.selectbox("Framework", [primary] + alts + ["5-Minute Rule", "ICE", "RAPID", "ASOFF", "Weighted Matrix", "STOP", "Alignment Resolution"], index=0)
fw_rationale = st.text_area("Framework rationale", value=ctx.get("framework_rationale", ""))

if st.button("Save Context Card"):
    chosen = fw_choice if override else primary
    payload = {
        "problem_alignment": prob_align,
        "metric_alignment": metric_align,
        "values_vs_tactical": values_vs,
        "alignment_notes": align_notes,
        "risk_scores": scores,
        "risk_total": total,
        "risk_category": cat,
        "risk_mitigation": mitigation,
        "undo_30_days": int(undo),
        "reversal_cost": rev_cost,
        "reversal_time_weeks": rev_weeks,
        "irreversible_commitments": irrev,
        "rev_type": suggested,
        "rev_type_override": rev_type,
        "framework_primary": primary,
        "framework_alternatives": ", ".join(alts),
        "framework_override": chosen if override else None,
        "framework_rationale": fw_rationale,
        "flags": {"values_based": values_based, "time_critical": time_critical, "high_complexity": high_complexity},
        "completed_by": actor,
    }
    db.upsert_context_card(decision_id, payload, actor)
    db.upsert_decision(
        {**decision, "exec_signoff": int(exec_signoff), "handoff_complete": int(handoff_complete), "status": "framework"},
        actor,
    )
    export_ctx = {**payload, "framework_primary": chosen, "rev_type": rev_type}
    md_export.export_context_card(decision_id, export_ctx, decision)
    st.session_state.selected_framework = chosen
    st.success(f"Saved. Use Framework page for **{chosen}**.")
