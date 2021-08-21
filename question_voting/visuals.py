import streamlit as st

from question_voting.authorization import is_authorized
from question_voting.global_states import ViewMode


def title_header():
    st.title("Live anonymous questions and answers")


def sidebar_title():
    st.sidebar.title("Admin Panel")


def sidebar_authorization_status():
    st.sidebar.subheader("Authorization Status")
    if not is_authorized():
        st.sidebar.warning("Unauthorized")
    else:
        st.sidebar.success("Authorized")


def create_change_view_widget():
    st.sidebar.subheader("View Polling Results")
    view_mode1, view_mode2 = st.sidebar.columns(2)
    view_mode1.button("Voting View Mode", on_click=ViewMode.voting)
    view_mode2.button("Results View Mode", on_click=ViewMode.reporting)
