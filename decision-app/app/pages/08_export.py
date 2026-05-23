"""Export Markdown and ZIP."""

import streamlit as st

from app.export import md_export
from app.storage import db
from app.ui_common import require_auth, sidebar_context

st.set_page_config(page_title="Export", layout="wide")
actor = require_auth()
if not actor:
    st.stop()
sidebar_context(actor)

st.title("Export")

decisions = db.list_decisions()
if not decisions:
    st.warning("No decisions to export.")
    st.stop()

decision_id = st.selectbox("Decision", [d["id"] for d in decisions], format_func=lambda i: next(d["title"] for d in decisions if d["id"] == i))
decision = db.get_decision(decision_id)
problem_id = decision.get("problem_id")

if st.button("Regenerate all exports"):
    if problem_id:
        ps = db.get_problem_statement(problem_id)
        if ps:
            md_export.export_problem_statement(problem_id, ps, actor)
        for rfc in db.list_rfcs(problem_id):
            md_export.export_rfc(rfc["id"], {**rfc, "author": actor})
    ctx = db.get_context_card(decision_id)
    if ctx:
        md_export.export_context_card(decision_id, ctx, decision)
    fw = db.get_framework_record(decision_id)
    if fw:
        if fw.get("framework_name") == "ICE":
            md_export.export_ice(decision_id, fw.get("data", {}), decision.get("title", ""))
        else:
            md_export.export_generic_framework(decision_id, fw["framework_name"], fw.get("data", {}))
    st.success("Exports regenerated under data/exports/")

zip_bytes = md_export.zip_exports(decision_id)
if zip_bytes:
    st.download_button(
        "Download ZIP",
        data=zip_bytes,
        file_name=f"{decision_id}-export.zip",
        mime="application/zip",
    )
else:
    st.info("No export files yet. Click Regenerate or save forms on other pages.")

from app.config import EXPORT_DIR

out = EXPORT_DIR / decision_id
if out.exists():
    st.markdown("**Files:**")
    for f in sorted(out.glob("*.md")):
        st.markdown(f"- `{f.name}`")
        with st.expander(f"Preview {f.name}"):
            st.markdown(f.read_text(encoding="utf-8")[:4000])
