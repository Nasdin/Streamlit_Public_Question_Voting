import base64
import dataclasses

import pandas as pd
import streamlit as st

from question_voting.authorization import must_be_authorized
from question_voting.global_states import GlobalPanels


def get_table_download_link(df, label, container):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download {label} csv file</a>'

    container.markdown(href, unsafe_allow_html=True)


def clean_data():
    new_statements = []
    all_comments = []
    for panel in GlobalPanels.panels():

        for statement_hash, statement in GlobalPanels.panels()[panel].statements.items():

            new_statement = dataclasses.asdict(statement)
            new_statement['panel'] = panel
            new_statement['hash'] = str(statement.hash)
            for comment in new_statement['comments']:
                comment['hash'] = str(comment['hash'])
                comment['parent'] = str(comment['parent'])
                comment['panel'] = panel
                all_comments.append(comment)
            new_statements.append(new_statement)

    all_questions = pd.DataFrame(new_statements)
    all_comments = pd.DataFrame(all_comments)

    return all_questions, all_comments


def generate_download_links_for_data(container):
    question_data, comment_data = clean_data()
    get_table_download_link(question_data, "question data", container)
    get_table_download_link(comment_data, "comment data", container)


@must_be_authorized
def create_data_export_widget():
    this_container = st.sidebar.container()
    this_container.button("Download QnA as CSV", on_click=generate_download_links_for_data, args=[this_container])
