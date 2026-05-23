"""Handoff checklist and start decision."""

import streamlit as st

from app.engine.ids import new_id
from app.storage import db
from app.ui_common import require_auth, sidebar_context

st.set_page_config(page_title="Handoff", layout="wide")
actor = require_auth()
if not actor:
    st.stop()
sidebar_context(actor)

st.title("Gate 1 — Handoff to Decision Tree")

problems = db.list_problems()
ready = [p for p in problems if p.get("rank") and p["rank"] <= 5]
if not ready:
    st.warning("No Top 5 problems. Promote on EB-25 page.")
    st.stop()

problem_id = st.selectbox("Problem", [p["id"] for p in ready], format_func=lambda i: next(p["title"] for p in ready if p["id"] == i))
st.session_state.problem_id = problem_id
p = db.get_problem(problem_id)
ps = db.get_problem_statement(problem_id)
rfcs = db.list_rfcs(problem_id)
final_rfcs = [r for r in rfcs if r.get("status") == "FINALIZED"]
total_options = sum(len([o for o in r.get("options", []) if o.get("name", "").strip()]) for r in rfcs)

checks = {
    "Top 5": bool(p.get("rank") and p["rank"] <= 5),
    "Problem Statement": bool(ps and ps.get("friction")),
    "Finalized RFC": len(final_rfcs) >= 1,
    "At least 3 options (across RFCs)": total_options >= 3,
}
for label, ok in checks.items():
    st.checkbox(label, value=ok, disabled=True)

expedited = st.checkbox("Expedited path (<48h)")
emergency = st.checkbox("Emergency path (<4h harm)")

all_ok = all(checks.values()) or emergency
if not all_ok:
    st.error("Handoff blocked until checklist passes (except emergency with retroactive docs).")

decision_title = st.text_input("Decision title", value=p["title"])
if st.button("Start decision", disabled=not (all_ok or emergency)):
    did = new_id(decision_title)
    rfc_ids = ",".join(r["id"] for r in (final_rfcs or rfcs)[:3])
    db.upsert_decision(
        {
            "id": did,
            "problem_id": problem_id,
            "rfc_ids": rfc_ids,
            "title": decision_title,
            "status": "state_gathering",
            "handoff_path": "emergency" if emergency else ("expedited" if expedited else "standard"),
            "handoff_complete": 1,
            "expedited": int(expedited),
            "emergency": int(emergency),
        },
        actor,
    )
    db.upsert_problem({**p, "status": "ready_for_decision"}, actor)
    st.session_state.decision_id = did
    st.success(f"Decision `{did}` created. Go to Context Card.")
