import streamlit as st

def add_new_question():
    with st.form(key="new_question"):
        new_question = st.text_area("Suggest a new question")
        to_add_question = st.form_submit_button("Add question")