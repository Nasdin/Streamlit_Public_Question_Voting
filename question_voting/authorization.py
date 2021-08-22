import streamlit as st

PASSWORD = st.secrets['admin_password']


def create_sidebar_admin_pass_input():
    st.sidebar.text_input("Admin Password", type="password", key="admin_password")


def is_authorized():
    if "admin_password" not in st.session_state:
        return False
    return st.session_state["admin_password"] == PASSWORD


def must_be_authorized(func):
    """ Decorator checks if user is authorized before running the function"""

    def authentication_function(*args, **kwargs):
        if is_authorized():
            return func(*args, **kwargs)
        else:
            st.warning("You are not authorized to run this function")

    return authentication_function
