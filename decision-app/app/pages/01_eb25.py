"""EB-25 backlog management."""

import streamlit as st

from app.engine.ids import new_id
from app.storage import db
from app.ui_common import EISENHOWER, PROBLEM_STATUSES, require_auth, sidebar_context

st.set_page_config(page_title="EB-25 Backlog", layout="wide")
actor = require_auth()
if not actor:
    st.stop()
sidebar_context(actor)

st.title("Gate 1 — EB-25 Backlog")
active_count = db.count_active_problems()
st.caption(f"Active problems: {active_count}/25 (Top 5 + Next 20)")

if active_count >= 25:
    st.warning("EB-25 cap reached (25). Archive or move items to Avoid before adding.")

problems = db.list_problems()
top5 = [p for p in problems if p.get("rank") and 1 <= p["rank"] <= 5]
next20 = [p for p in problems if p.get("rank") and 6 <= p["rank"] <= 25]
other = [p for p in problems if not p.get("rank") or p["rank"] > 25]

with st.expander("Add problem", expanded=False):
    title = st.text_input("Title / summary")
    summary = st.text_area("Brief summary")
    eisenhower = st.selectbox("Eisenhower", EISENHOWER)
    owner = st.text_input("Owner")
    rank = st.number_input("Rank (1-25, leave 0 for unranked)", min_value=0, max_value=25, value=0)
    if st.button("Save problem"):
        if active_count >= 25:
            st.error("Cannot add: at capacity.")
        elif not title.strip():
            st.error("Title required.")
        else:
            pid = new_id(title, "prob")
            db.upsert_problem(
                {
                    "id": pid,
                    "title": title.strip(),
                    "summary": summary,
                    "eisenhower": eisenhower,
                    "owner": owner,
                    "rank": rank if rank > 0 else None,
                    "status": "raw",
                },
                actor,
            )
            st.session_state.problem_id = pid
            st.success(f"Created {pid}")
            st.rerun()


def _table(rows, label):
    st.subheader(label)
    if not rows:
        st.caption("None")
        return
    for p in rows:
        cols = st.columns([3, 2, 2, 2, 1])
        cols[0].write(f"**#{p.get('rank', '—')}** {p['title']}")
        cols[1].write(p.get("eisenhower", ""))
        cols[2].write(p.get("owner", ""))
        cols[3].write(p.get("status", ""))
        if cols[4].button("Select", key=f"sel_{p['id']}"):
            st.session_state.problem_id = p["id"]
            st.rerun()


_table(top5, "Top 5 (active)")
_table(next20, "Next 20 (waiting)")
if other:
    _table(other, "Unranked / other")

if st.session_state.get("problem_id"):
    p = db.get_problem(st.session_state.problem_id)
    if p:
        st.divider()
        st.markdown(f"**Selected:** `{p['id']}` — {p['title']}")
        new_rank = st.number_input("Update rank", min_value=0, max_value=25, value=p.get("rank") or 0)
        new_status = st.selectbox("Status", PROBLEM_STATUSES, index=PROBLEM_STATUSES.index(p.get("status", "raw")) if p.get("status") in PROBLEM_STATUSES else 0)
        if st.button("Update selected problem"):
            p["rank"] = new_rank if new_rank > 0 else None
            p["status"] = new_status
            db.upsert_problem(p, actor)
            st.success("Updated")
            st.rerun()
