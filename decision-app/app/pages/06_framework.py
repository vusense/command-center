"""Dynamic framework worksheets."""

import streamlit as st

from app.export import md_export
from app.storage import db
from app.ui_common import FRAMEWORKS, needs_retrospection, require_auth, sidebar_context

st.set_page_config(page_title="Framework", layout="wide")
actor = require_auth()
if not actor:
    st.stop()
sidebar_context(actor)

st.title("Gate 2 — Framework Application")

decisions = [d for d in db.list_decisions() if d.get("status") != "complete"]
if not decisions:
    st.warning("No active decisions.")
    st.stop()

decision_id = st.selectbox("Decision", [d["id"] for d in decisions], format_func=lambda i: next(d["title"] for d in decisions if d["id"] == i))
st.session_state.decision_id = decision_id
decision = db.get_decision(decision_id)
ctx = db.get_context_card(decision_id)
if not ctx:
    st.warning("Complete the Context Card first.")
    st.stop()

default_fw = (
    st.session_state.get("selected_framework")
    or ctx.get("framework_override")
    or ctx.get("framework_primary")
    or "ICE"
)
framework = st.selectbox("Framework", FRAMEWORKS, index=FRAMEWORKS.index(default_fw) if default_fw in FRAMEWORKS else 1)
record = db.get_framework_record(decision_id)
data = record.get("data", {}) if record else {}

if framework == "ICE":
    st.markdown("### ICE Scorecard")
    options = data.get("scorecard", [{"option": "A", "impact": 5, "confidence": 5, "ease": 5} for _ in range(3)])
    rows = []
    for i, row in enumerate(options):
        st.markdown(f"**Option {row.get('option', chr(65+i))}**")
        c1, c2, c3, c4 = st.columns(4)
        opt = c1.text_input("Label", value=row.get("option", chr(65 + i)), key=f"ol_{i}")
        imp = c2.number_input("Impact", 1, 10, int(row.get("impact", 5)), key=f"oi_{i}")
        conf = c3.number_input("Confidence", 1, 10, int(row.get("confidence", 5)), key=f"oc_{i}")
        ease = c4.number_input("Ease", 1, 10, int(row.get("ease", 5)), key=f"oe_{i}")
        rows.append({"option": opt, "impact": imp, "confidence": conf, "ease": ease, "ice_score": imp * conf * ease})
    st.dataframe(rows, use_container_width=True)
    selected = st.selectbox("Selected option", [r["option"] for r in rows])
    rationale = st.text_area("Rationale", value=data.get("rationale", ""))
    impl = st.text_area("Implementation notes", value=data.get("implementation_notes", ""))
    sign_a = st.text_input("Cofounder A sign-off", value=data.get("signoff_a", ""))
    sign_b = st.text_input("Cofounder B sign-off", value=data.get("signoff_b", ""))
    save_data = {
        "scorecard": rows,
        "selected_option": selected,
        "rationale": rationale,
        "implementation_notes": impl,
        "signoff_a": sign_a,
        "signoff_b": sign_b,
    }
elif framework == "5-Minute Rule":
    st.markdown("### 5-Minute Rule Log")
    save_data = {
        "position_a": st.text_area("Cofounder A position", value=data.get("position_a", "")),
        "position_b": st.text_area("Cofounder B position", value=data.get("position_b", "")),
        "aligned": st.checkbox("Aligned", value=data.get("aligned", True)),
        "decision": st.text_area("Decision", value=data.get("decision", "")),
    }
elif framework == "RAPID":
    st.markdown("### RAPID Log")
    save_data = {
        "recommend": st.text_area("Recommend", value=data.get("recommend", "")),
        "agree": st.text_area("Agree", value=data.get("agree", "")),
        "perform": st.text_area("Perform", value=data.get("perform", "")),
        "input": st.text_area("Input", value=data.get("input", "")),
        "decide": st.text_area("Decide", value=data.get("decide", "")),
    }
elif framework == "ASOFF":
    st.markdown("### ASOFF Worksheet")
    save_data = {
        "assess": st.text_area("Assess", value=data.get("assess", "")),
        "stake": st.text_area("Stake positions", value=data.get("stake", "")),
        "options": st.text_area("Options (min 3)", value=data.get("options", "")),
        "filter": st.text_area("Filter", value=data.get("filter", "")),
        "finalize": st.text_area("Finalize", value=data.get("finalize", "")),
    }
elif framework == "STOP":
    st.markdown("### STOP Protocol")
    save_data = {
        "stop": st.text_area("S — Stop", value=data.get("stop", "")),
        "think": st.text_area("T — Think (private positions)", value=data.get("think", "")),
        "observe": st.text_area("O — Observe data", value=data.get("observe", "")),
        "proceed": st.text_area("P — Proceed", value=data.get("proceed", "")),
    }
elif framework == "Weighted Matrix":
    st.markdown("### Weighted Decision Matrix")
    criteria = st.text_area("Criteria (one per line)", value=data.get("criteria", "Cost\nTimeline\nRisk"))
    save_data = {"criteria": criteria, "matrix_notes": st.text_area("Scores & weights", value=data.get("matrix_notes", ""))}
elif framework == "Alignment Resolution":
    st.markdown("### Alignment Resolution Log")
    save_data = {
        "discrepancy": st.text_area("Discrepancy", value=data.get("discrepancy", "")),
        "resolution": st.text_area("Resolution", value=data.get("resolution", "")),
    }
else:
    save_data = {"notes": st.text_area("Notes", value=str(data))}

rev_type = ctx.get("rev_type_override") or ctx.get("rev_type", "II")
if needs_retrospection(framework, rev_type):
    st.warning("Retrospection is **mandatory** for this framework/decision type.")

if st.button("Save framework worksheet"):
    db.upsert_framework_record(decision_id, framework, save_data, actor)
    if framework == "ICE":
        md_export.export_ice(decision_id, save_data, decision.get("title", ""))
    else:
        md_export.export_generic_framework(decision_id, framework, save_data)
    db.upsert_decision({**decision, "status": "register"}, actor)
    st.success("Saved. Complete Register and Export.")

    if needs_retrospection(framework, rev_type):
        st.info("Complete retrospection on the Register page.")
