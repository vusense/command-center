"""Decision register and retrospection."""

import streamlit as st

from app.storage import db
from app.ui_common import needs_retrospection, require_auth, sidebar_context

st.set_page_config(page_title="Register", layout="wide")
actor = require_auth()
if not actor:
    st.stop()
sidebar_context(actor)

st.title("Decision Register")

entries = db.list_register()
st.subheader("Register")
if entries:
    st.dataframe(
        [
            {
                "ID": e["decision_id"],
                "Date": e.get("date"),
                "Title": e.get("title"),
                "Framework": e.get("framework"),
                "Risk": e.get("risk_level"),
                "Rev": e.get("reversibility"),
                "Outcome": e.get("outcome"),
                "Status": e.get("status"),
            }
            for e in entries
        ],
        use_container_width=True,
    )
else:
    st.caption("No register entries yet.")

st.divider()
st.subheader("Add / update entry")

decisions = db.list_decisions()
if not decisions:
    st.stop()

decision_id = st.selectbox("Decision", [d["id"] for d in decisions], format_func=lambda i: next(d["title"] for d in decisions if d["id"] == i))
decision = db.get_decision(decision_id)
ctx = db.get_context_card(decision_id) or {}
fw_rec = db.get_framework_record(decision_id)
framework = fw_rec.get("framework_name") if fw_rec else (ctx.get("framework_override") or ctx.get("framework_primary", ""))

from datetime import date

col1, col2 = st.columns(2)
with col1:
    outcome = st.selectbox("Outcome", ["", "SUCCESSFUL", "LEARNING", "FAILED"])
    status = st.selectbox("Status", ["ACTIVE", "COMPLETE", "PAUSED"], index=1)
with col2:
    risk_level = st.selectbox("Risk level", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], index=["LOW", "MEDIUM", "HIGH", "CRITICAL"].index(ctx.get("risk_category", "MEDIUM")) if ctx.get("risk_category") in ("LOW", "MEDIUM", "HIGH", "CRITICAL") else 1)
    rev = st.selectbox("Reversibility", ["I", "II", "III", "IV"], index=["I", "II", "III", "IV"].index(ctx.get("rev_type_override") or ctx.get("rev_type") or "II") if ctx else 1)

if st.button("Save register row"):
    db.upsert_register_entry(
        {
            "decision_id": decision_id,
            "date": date.today().isoformat(),
            "title": decision.get("title"),
            "framework": framework,
            "risk_level": risk_level,
            "reversibility": rev,
            "outcome": outcome,
            "status": status,
            "document_link": f"data/exports/{decision_id}/",
        },
        actor,
    )
    if status == "COMPLETE":
        db.upsert_decision({**decision, "status": "complete"}, actor)
    st.success("Register updated")
    st.rerun()

st.divider()
st.subheader("Retrospection")
if ctx and fw_rec:
    rev_type = ctx.get("rev_type_override") or ctx.get("rev_type", "II")
    mandatory = needs_retrospection(fw_rec.get("framework_name", ""), rev_type)
    if mandatory:
        st.caption("Required for this decision.")
    retro = db.get_retrospection(decision_id)
    retro_data = retro.get("data", {}) if retro else {}
    what_worked = st.text_area("What worked?", value=retro_data.get("what_worked", ""))
    what_failed = st.text_area("What failed?", value=retro_data.get("what_failed", ""))
    framework_effective = st.selectbox("Framework effective?", ["Yes", "Partially", "No"], index=0)
    if st.button("Save retrospection"):
        db.upsert_retrospection(
            decision_id,
            {
                "what_worked": what_worked,
                "what_failed": what_failed,
                "framework_effective": framework_effective,
            },
            completed=bool(what_worked or what_failed),
            actor=actor,
        )
        st.success("Retrospection saved.")

st.subheader("Summary")
entries = db.list_register()
st.write(f"Total decisions: {len(entries)}")
by_fw: dict[str, int] = {}
for e in entries:
    f = e.get("framework") or "unknown"
    by_fw[f] = by_fw.get(f, 0) + 1
if by_fw:
    st.bar_chart(by_fw)
