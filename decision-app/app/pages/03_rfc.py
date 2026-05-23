"""RFC with minimum 3 options."""

import streamlit as st

from app.engine.ids import new_id
from app.export import md_export
from app.storage import db
from app.ui_common import require_auth, sidebar_context

st.set_page_config(page_title="RFC", layout="wide")
actor = require_auth()
if not actor:
    st.stop()
sidebar_context(actor)

st.title("Gate 1 — RFC")

problems = [p for p in db.list_problems() if p.get("status") != "avoid"]
if not problems:
    st.warning("No problems available.")
    st.stop()

problem_id = st.selectbox(
    "Problem",
    [p["id"] for p in problems],
    index=0 if not st.session_state.get("problem_id") else [p["id"] for p in problems].index(st.session_state.problem_id) if st.session_state.get("problem_id") in [p["id"] for p in problems] else 0,
    format_func=lambda i: next(p["title"] for p in problems if p["id"] == i),
)
st.session_state.problem_id = problem_id

rfcs = db.list_rfcs(problem_id)
rfc_id = st.selectbox(
    "RFC",
    ["(new)"] + [r["id"] for r in rfcs],
    format_func=lambda x: x if x == "(new)" else x,
)
existing = db.get_rfc(rfc_id) if rfc_id != "(new)" else None
options = existing.get("options", []) if existing else [{"name": "", "description": ""} for _ in range(3)]
while len(options) < 3:
    options.append({"name": "", "description": ""})

with st.form("rfc_form"):
    title = st.text_input("RFC title", value=existing.get("title", "") if existing else "")
    status = st.selectbox("Status", ["DRAFT", "IN REVIEW", "FINALIZED"], index=["DRAFT", "IN REVIEW", "FINALIZED"].index(existing.get("status", "DRAFT")) if existing else 0)
    proposed = st.text_area("1. Proposed Solution", value=existing.get("proposed_solution", "") if existing else "", height=100)
    design = st.text_area("2. Detailed Design", value=existing.get("detailed_design", "") if existing else "", height=100)
    cost = st.text_area("3. Cost & Resources", value=existing.get("cost_resources", "") if existing else "", height=80)
    tradeoffs = st.text_area("4. Trade-offs & Risks", value=existing.get("tradeoffs_risks", "") if existing else "", height=80)
    st.markdown("**5. Alternatives (minimum 3)**")
    new_options = []
    for i in range(max(3, len(options))):
        if i >= 3 and i >= len(options):
            break
        opt = options[i] if i < len(options) else {"name": "", "description": ""}
        st.markdown(f"**Option {chr(65 + i)}**")
        name = st.text_input(f"Name {chr(65 + i)}", value=opt.get("name", ""), key=f"on_{i}")
        desc = st.text_area(f"Description {chr(65 + i)}", value=opt.get("description", ""), key=f"od_{i}", height=60)
        new_options.append({"name": name, "description": desc})
    extra = st.number_input("Extra option slots", min_value=0, max_value=3, value=0)
    for j in range(extra):
        idx = len(new_options)
        st.markdown(f"**Option {chr(65 + idx)}**")
        new_options.append(
            {
                "name": st.text_input(f"Name extra {j}", key=f"exn_{j}"),
                "description": st.text_area(f"Desc extra {j}", key=f"exd_{j}", height=60),
            }
        )
    comments = st.text_area("Reviewer comments", value=existing.get("reviewer_comments", "") if existing else "")
    save = st.form_submit_button("Save RFC")

if save:
    filled = [o for o in new_options if o.get("name", "").strip()]
    if len(filled) < 3:
        st.error("Need at least 3 options with names.")
    else:
        rid = rfc_id if rfc_id != "(new)" else new_id(title or "rfc", "rfc")
        payload = {
            "id": rid,
            "problem_id": problem_id,
            "title": title,
            "status": status,
            "proposed_solution": proposed,
            "detailed_design": design,
            "cost_resources": cost,
            "tradeoffs_risks": tradeoffs,
            "options": filled,
            "reviewer_comments": comments,
            "author": actor,
        }
        db.upsert_rfc(payload, actor)
        md_export.export_rfc(rid, payload)
        st.session_state.rfc_id = rid
        if status == "FINALIZED":
            db.upsert_problem({**db.get_problem(problem_id), "status": "rfc_finalized"}, actor)
        st.success(f"Saved {rid}")
