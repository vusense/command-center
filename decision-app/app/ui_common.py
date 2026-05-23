"""Shared Streamlit helpers: auth, session context, sidebar."""

import os
from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
import yaml

from app.config import ROOT
from app.storage import db

db.init_db()

ALIGNMENT_MAP = {"YES": "FULL", "NO": "NONE", "PARTIAL": "PARTIAL"}
ALIGNMENT_UI = ["YES", "PARTIAL", "NO"]
EISENHOWER = [
    "Urgent + Important",
    "Not Urgent + Important",
    "Urgent + Not Important",
    "Not Urgent + Not Important",
]
FRAMEWORKS = [
    "5-Minute Rule",
    "ICE",
    "RAPID",
    "ASOFF",
    "Weighted Matrix",
    "STOP",
    "Alignment Resolution",
]
PROBLEM_STATUSES = [
    "raw",
    "identification",
    "rfc_draft",
    "rfc_review",
    "rfc_finalized",
    "ready_for_decision",
]
MANDATORY_RETRO_FRAMEWORKS = {"STOP", "Alignment Resolution"}


def load_authenticator():
    cred_path = ROOT / "credentials.yaml"
    if cred_path.exists():
        with open(cred_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return stauth.Authenticate(
            config["credentials"],
            config["cookie"]["name"],
            config["cookie"]["key"],
            config["cookie"]["expiry_days"],
        )
    # Fallback: env-based single user
    user = os.environ.get("AUTH_USERNAME", "cofounder")
    pwd = os.environ.get("AUTH_PASSWORD", "changeme")
    hashed = stauth.Hasher.hash([pwd])[0]
    config = {
        "credentials": {
            "usernames": {
                user: {"name": user, "password": hashed},
            }
        },
        "cookie": {"name": "vusense_decision", "key": "vusense_key_change_me", "expiry_days": 30},
    }
    return stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )


def require_auth() -> str | None:
    authenticator = load_authenticator()
    authenticator.login(location="main")
    name = st.session_state.get("name")
    auth_status = st.session_state.get("authentication_status")
    if auth_status is False:
        st.error("Invalid username or password")
        return None
    if auth_status is None:
        st.info("Sign in to use the Vusense Decision App")
        return None
    return name or st.session_state.get("username", "user")


def init_session_keys():
    defaults = {
        "problem_id": None,
        "rfc_id": None,
        "decision_id": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def sidebar_context(actor: str):
    st.sidebar.markdown("### Working context")
    problems = [p for p in db.list_problems() if p.get("rank") and p["rank"] <= 5]
    if problems:
        st.sidebar.caption("Top 5")
        for p in problems[:5]:
            if st.sidebar.button(p["title"][:40], key=f"sp_{p['id']}"):
                st.session_state.problem_id = p["id"]
    decisions = db.list_decisions()
    active = [d for d in decisions if d.get("status") != "complete"]
    if active:
        st.sidebar.caption("In-progress decisions")
        for d in active[:5]:
            if st.sidebar.button(d["title"][:40], key=f"sd_{d['id']}"):
                st.session_state.decision_id = d["id"]
                st.session_state.problem_id = d.get("problem_id")
    st.sidebar.divider()
    st.sidebar.caption(f"Signed in: {actor}")
    if st.session_state.problem_id:
        st.sidebar.text(f"Problem: {st.session_state.problem_id}")
    if st.session_state.decision_id:
        st.sidebar.text(f"Decision: {st.session_state.decision_id}")


def alignment_to_engine(ui_val: str) -> str:
    return ALIGNMENT_MAP.get(ui_val, "PARTIAL")


def needs_retrospection(framework: str, rev_type: str) -> bool:
    if framework in MANDATORY_RETRO_FRAMEWORKS:
        return True
    return rev_type in ("III", "IV")
