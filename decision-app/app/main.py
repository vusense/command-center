"""Vusense Decision App — home and quick start."""

import streamlit as st

from app.storage import db as _db
from app.ui_common import init_session_keys, require_auth, sidebar_context

st.set_page_config(
    page_title="Vusense Decision",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

actor = require_auth()
if not actor:
    st.stop()

init_session_keys()
sidebar_context(actor)

st.title("Vusense Decision App")
st.markdown(
    "Executive **Problem Discovery** (Gate 1) and **Decision Tree** (Gate 2). "
    "Use the sidebar pages to move through the process."
)

with st.expander("Quick start", expanded=False):
    st.markdown(
        """
1. **EB-25 Backlog** — capture and rank problems (max 25 active).
2. **Problem Statement** — formalize the selected problem.
3. **RFC** — document solution options (minimum 3).
4. **Handoff** — start a decision when ready.
5. **Context Card** — alignment, risk, reversibility, framework selection.
6. **Framework** — complete the chosen worksheet (ICE, ASOFF, etc.).
7. **Register** — track outcomes.
8. **Export** — download Markdown / ZIP for Obsidian or board packs.
        """
    )

col1, col2 = st.columns(2)
with col1:
    active = [p for p in _db.list_problems() if p.get("status") not in ("avoid", "archived")]
    st.metric("Active problems", len(active))
with col2:
    decisions = _db.list_decisions()
    st.metric("Decisions in progress", len([d for d in decisions if d.get("status") != "complete"]))

st.info("Select a page from the sidebar to continue.")
