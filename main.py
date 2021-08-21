import time

import streamlit as st

from question_voting.authorization import create_sidebar_admin_pass_input, is_authorized
from question_voting.data_export import create_data_export_widget
from question_voting.global_states import GlobalPanels, ViewMode
from question_voting.panels import create_main_panel_admin_widget, DisplayStatementsInPanel, \
    create_clear_panel_container, DisplayReportingModeInPanel
from question_voting.questions import create_admin_add_question_form
from question_voting.visuals import title_header, sidebar_title, sidebar_authorization_status, create_change_view_widget

PANELS = 5

if "selected_panel" not in st.session_state:
    st.session_state['selected_panel'] = 0


def main() -> list:
    things_to_update = []
    title_header()
    statement_container = st.container()
    things_to_build = [DisplayStatementsInPanel(statement_container, st.session_state['selected_panel']),
                       DisplayReportingModeInPanel(statement_container, st.session_state['selected_panel'])
                       ]
    viewing_mode = ViewMode.mode()
    for thing in things_to_build:
        if thing.only_seen_in == viewing_mode:
            thing.build()
            things_to_update.append(thing)
        things_to_update.append(thing)
    return things_to_update


def main_updater_forever(to_update_things: list):
    viewing_mode = ViewMode.mode()

    while True:
        for thing in to_update_things:
            if thing.only_seen_in == viewing_mode:
                thing.update()
        time.sleep(2)


def sidebar_panel_status():
    st.sidebar.subheader("Currently Showing Panel")
    st.sidebar.write(st.session_state['selected_panel'] + 1)


def main_sidebar():
    sidebar_panel_status()
    create_main_panel_admin_widget(PANELS)
    sidebar_title()
    sidebar_authorization_status()
    create_sidebar_admin_pass_input()
    if is_authorized():
        create_admin_add_question_form()
        create_clear_panel_container()
        create_change_view_widget()
        create_data_export_widget()


if __name__ == '__main__':
    st.set_page_config("Anonymous QnA", initial_sidebar_state='collapsed')

    main_sidebar()
    to_update = main()
    main_updater_forever(to_update)
