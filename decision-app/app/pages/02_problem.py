"""Problem Statement form."""

import streamlit as st

from app.export import md_export
from app.storage import db
from app.ui_common import require_auth, sidebar_context

st.set_page_config(page_title="Problem Statement", layout="wide")
actor = require_auth()
if not actor:
    st.stop()
sidebar_context(actor)

st.title("Gate 1 — Problem Statement")

problems = db.list_problems()
if not problems:
    st.warning("Add a problem on the EB-25 page first.")
    st.stop()

ids = [p["id"] for p in problems]
default_idx = ids.index(st.session_state.problem_id) if st.session_state.get("problem_id") in ids else 0
problem_id = st.selectbox("Problem", ids, index=default_idx, format_func=lambda i: next(p["title"] for p in problems if p["id"] == i))
st.session_state.problem_id = problem_id
p = db.get_problem(problem_id)
st.caption(f"**{p['title']}**")

existing = db.get_problem_statement(problem_id) or {}
rank = p.get("rank") or 0

with st.form("problem_statement"):
    context = st.text_area("1. Context", value=existing.get("context", ""), height=120)
    friction = st.text_area("2. The Friction (no solutions)", value=existing.get("friction", ""), height=120)
    impact = st.text_area("3. The Impact", value=existing.get("impact", ""), height=100)
    constraints = st.text_area("4. Constraints", value=existing.get("constraints", ""), height=80)
    success = st.text_area("5. Success Criteria", value=existing.get("success_criteria", ""), height=80)
    tech_refs = st.text_input("Related technical stack docs", value=existing.get("tech_refs", ""))
    repos = st.text_input("Repos impacted", value=existing.get("repos_impacted", ""))
    submitted = st.form_submit_button("Save Problem Statement")
    if submitted:
        data = {
            "context": context,
            "friction": friction,
            "impact": impact,
            "constraints": constraints,
            "success_criteria": success,
            "tech_refs": tech_refs,
            "repos_impacted": repos,
            "eb25_rank": rank if rank else None,
        }
        db.upsert_problem_statement(problem_id, data, actor)
        md_export.export_problem_statement(problem_id, data, actor)
        st.success("Saved and exported Markdown.")
