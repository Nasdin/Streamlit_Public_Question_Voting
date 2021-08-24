import dataclasses

import pandas as pd
import streamlit as st

from question_voting.authorization import must_be_authorized
from question_voting.global_states import GlobalPanels, GlobalSharedStatements
from question_voting.statement import DisplayStatement

if "selected_panel" not in st.session_state:
    st.session_state['selected_panel'] = 0


def get_panels():
    return sorted(list(GlobalPanels.panels().keys()))


def _next_panel_count():
    panel_list = get_panels()
    panel_list.sort()
    if panel_list:
        previous_number = panel_list[0]
        panel_list.pop(0)
    else:
        return 0
    for i in panel_list:
        if i != previous_number + 1:
            return previous_number + 1
        previous_number = i
    return previous_number + 1


def create_panel():
    GlobalPanels.panels()[_next_panel_count()] = GlobalSharedStatements(_next_panel_count())


def create_panels(total_panels):
    panel_count = len(get_panels())
    for i in range(max(total_panels - panel_count, 0)):
        create_panel()


def _get_panel_to_replace_deleted_with(panel_to_delete):
    to_replace_with = get_panels()[0]
    if panel_to_delete == to_replace_with:
        if len(get_panels()) > 1:
            return get_panels()[1]
        st.write("Hel")
        return None
    return to_replace_with


def _clear_panel(panel_id: int):
    if panel_id in GlobalPanels.panels().keys():
        GlobalPanels.panels()[panel_id].clear()


def current_panel():
    return GlobalPanels.panels()[st.session_state['selected_panel']]


@must_be_authorized
def clear_panel():
    if "clear_panel" in st.session_state:
        panel_to_delete = st.session_state['clear_panel']
        _clear_panel(panel_to_delete)
        st.warning(f"Wiped panel {panel_to_delete + 1}")


def create_create_panel_container(create_container):
    create_container.radio("Change Panel View", options=get_panels(), key='selected_panel',
                           format_func=lambda x: str(x + 1))


def create_clear_panel_container():
    with st.sidebar.form("Clear containers"):
        st.selectbox("Clear Panel", options=get_panels(),
                     key="clear_panel", format_func=lambda x: str(x + 1))
        st.form_submit_button("Clear", on_click=clear_panel)


def create_main_panel_admin_widget(panel_count):
    st.sidebar.subheader("Multi Panel Settings")
    select_container = st.sidebar.empty()
    create_panels(panel_count)
    create_create_panel_container(select_container)


class DisplayStatementsInPanel(object):
    only_seen_in = "VOTING"

    def __init__(self, parent_container, panel):

        self.statements_built = {}
        self.empty = parent_container.empty()
        self.container = self.empty.container()
        self.panel = panel
        self.stale_preventor = None

    def build(self):
        self.container.header(f"Questions for Panel: {st.session_state['selected_panel'] + 1}")
        self.stale_preventor = self.container.empty()

    def update(self):
        has_updates = False
        for statement_hash, statement in GlobalPanels.panels()[self.panel].statements.items():
            has_updates = True
            if statement_hash not in self.statements_built:
                displayed_statement = DisplayStatement(self.container, statement)
                displayed_statement.build()
                self.statements_built[statement_hash] = displayed_statement

            else:
                displayed_statement = self.statements_built[statement_hash]
            displayed_statement.update()
        if not has_updates:
            self.stale_preventor.write("There are no questions posted")


class DisplayReportingModeInPanel(object):
    only_seen_in = "REPORTING"

    def __init__(self, parent_container, panel):

        self.panel = panel
        self.stale_preventor = None
        self.empty = parent_container.empty()
        self.container = self.empty.container()

    def build(self):
        self.container.header(f"Reporting for Panel: {st.session_state['selected_panel'] + 1}")
        self.stale_preventor = self.container.empty()

        self.question_highest_upvotes = self.container.empty()
        self.question_highest_downvotes = self.container.empty()
        self.question_highest_overall = self.container.empty()
        self.question_lowest_overall = self.container.empty()
        self.question_most_comments = self.container.empty()

        self.question_most_upvoted_comments = self.container.empty()
        self.question_most_downvoted_comments = self.container.empty()

    def update(self):
        has_updates = False
        new_statements = []
        all_comments = []
        for statement_hash, statement in GlobalPanels.panels()[self.panel].statements.items():
            has_updates = True
            new_statement = dataclasses.asdict(statement)
            new_statement['hash'] = str(statement.hash)
            for comment in new_statement['comments']:
                comment['hash'] = str(comment['hash'])
                comment['parent'] = str(comment['parent'])
                all_comments.append(comment)
            new_statements.append(new_statement)

        all_questions = pd.DataFrame(new_statements)
        all_comments = pd.DataFrame(all_comments)

        question_highest_upvotes = self.question_highest_upvotes.container()
        question_highest_downvotes = self.question_highest_downvotes.container()
        question_highest_overall = self.question_highest_overall.container()
        question_lowest_overall = self.question_lowest_overall.container()
        question_most_comments = self.question_most_comments.container()

        question_highest_upvotes.header("Question Analysis")

        if all_questions.shape[0] > 0:
            upvote_chart, downvote_chart = question_highest_upvotes.columns(2)
            upvote_chart.subheader("Upvotes Live (Top 5)")
            upvotes_df = all_questions.sort_values('votes', ascending=False).head(5).set_index('text')['votes']
            upvote_chart.bar_chart(upvotes_df)

            downvote_chart.subheader("Downvotes Live (Top 5)")
            downvotes_df = all_questions.sort_values('downvotes', ascending=False).head(5).set_index('text')[
                'downvotes']
            downvote_chart.bar_chart(downvotes_df)

            question_highest_upvotes.subheader("Most comments Live (Top 5)")
            all_questions['comment_count'] = all_questions['comments'].apply(lambda x: len(x))
            most_comments_df = all_questions.sort_values('comment_count', ascending=False).head(5).set_index('text')[
                'comment_count']
            question_highest_upvotes.bar_chart(most_comments_df)

            question_highest_upvotes.subheader("Question with highest upvote")
            question_highest_upvotes.write("##### Question")
            question_highest_upvotes.write(all_questions.loc[all_questions['votes'].argmax(), 'text'])
            question_highest_upvotes.write(f"Upvotes: {all_questions['votes'].max()}")

            question_highest_downvotes.subheader("Question with highest downvotes")
            question_highest_downvotes.write("##### Question")
            question_highest_downvotes.write(all_questions.loc[all_questions['downvotes'].argmax(), 'text'])
            question_highest_downvotes.write(f"Downvotes: {all_questions['downvotes'].max()}")

            question_highest_overall.subheader("Question with highest overall")
            question_highest_overall.write("##### Question")
            question_highest_overall.write(
                all_questions.loc[((all_questions['downvotes'] * -1) + all_questions['votes']).argmax(), 'text'])
            question_highest_overall.write(
                f"Highest overall: {((all_questions['downvotes'] * -1) + all_questions['votes']).max()}")

            question_lowest_overall.subheader("Question with lowest overall")
            question_lowest_overall.write("##### Question")
            question_lowest_overall.write(
                all_questions.loc[((all_questions['downvotes'] * -1) + all_questions['votes']).argmin(), 'text'])
            question_lowest_overall.write(
                f"Lowest overall: {((all_questions['downvotes'] * -1) + all_questions['votes']).min()}")

            question_most_comments.subheader("Question with most comments")
            question_most_comments.write("##### Question")
            question_most_comments.write(
                all_questions.loc[all_questions['comments'].apply(lambda x: len(x)).argmax(), 'text'])
            question_most_comments.write(f"Most comments: {all_questions['comments'].apply(lambda x: len(x)).max()}")

        else:
            question_highest_upvotes.subheader("No question has been posted yet")

        question_most_upvoted_comments = self.question_most_upvoted_comments.container()
        question_most_downvoted_comments = self.question_most_downvoted_comments.container()

        question_most_upvoted_comments.header("Comments analysis")

        if all_comments.shape[0] > 0:
            question_most_upvoted_comments.subheader("Highest upvoted comment")
            question_most_upvoted_comments.write("##### Comment")
            question_most_upvoted_comments.write(all_comments.loc[all_comments['votes'].argmax(), 'text'])
            question_most_upvoted_comments.write(f"Upvotes: {all_comments['votes'].max()}")

            question_most_downvoted_comments.subheader("Highest downvoted comment")
            question_most_downvoted_comments.write("##### Comment")
            question_most_downvoted_comments.write(all_comments.loc[all_comments['downvotes'].argmax(), 'text'])
            question_most_downvoted_comments.write(f"Downvotes: {all_comments['downvotes'].max()}")

            upvote_chart, downvote_chart = question_most_downvoted_comments.columns(2)
            upvote_chart.subheader("Upvotes comments Live (Top 5)")
            upvotes_df = all_comments.sort_values('votes', ascending=False).head(5).set_index('text')['votes']
            upvote_chart.bar_chart(upvotes_df)

            downvote_chart.subheader("Downvotes comments Live (Top 5)")
            downvotes_df = all_comments.sort_values('downvotes', ascending=False).head(5).set_index('text')['downvotes']
            downvote_chart.bar_chart(downvotes_df)
        else:
            question_most_upvoted_comments.subheader("No comments have been added yet")

        if not has_updates:
            self.stale_preventor.write("There are no questions posted")
