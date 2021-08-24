import streamlit as st

from question_voting.authorization import must_be_authorized
from question_voting.panels import GlobalPanels
from question_voting.statement import Question


def create_admin_add_question_form():
    with st.sidebar.form(key="add_question_form"):
        st.subheader("Add a new question")
        st.text_area("Write your question here", key="new_question_text")
        st.form_submit_button(
            "Add question",
            help=f"Question to be posted to this panel: {st.session_state['selected_panel'] + 1}",
            on_click=add_question,
            kwargs={
                "all_panels": GlobalPanels,
                "question_text_key": "new_question_text",
            },
        )


def _add_question(all_panels: GlobalPanels, chosen_panel: int, question_text):
    panel_data_plane = all_panels.panels()[chosen_panel].statements
    question = Question(question_text)
    panel_data_plane[question.hash] = question


@must_be_authorized
def add_question(all_panels, question_text_key):
    question_text = st.session_state[question_text_key]
    if question_text.strip() != "":
        _add_question(all_panels, st.session_state["selected_panel"], question_text)
    st.sidebar.info(f"Added question")
