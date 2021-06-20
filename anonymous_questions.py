import hashlib
import time

import streamlit as st

st.set_page_config("Mendaki Anonymous questions voting")


@st.cache(allow_output_mutation=True, persist=True)
def questions_list():
    return []


@st.cache(allow_output_mutation=True)
def questions_hash_list():
    return []


@st.cache(allow_output_mutation=True, persist=True)
def questions_votes():
    return []


@st.cache(allow_output_mutation=True)
def questions_to_be_deleted():
    return []


def add_question(question_text):
    question_hashed = hash_question(question_text)

    if question_hashed in questions_hash_list():
        st.warning("Question already added")
    else:
        q_l = questions_list()
        q_v = questions_votes()
        q_l.append(question_text)
        q_v.append(0)
        questions_hash_list().append(question_hashed)
        st.success("Your question has been added!")


def vote_question(index_to_vote, header_container):
    q_v = questions_votes()
    q_v[index_to_vote] = q_v[index_to_vote] + 1
    header_container.success("Thanks for voting")


def delete_question(question_index):
    q_l = questions_list()
    q_l.remove(question_index)
    q_v = questions_votes()
    q_v.remove(question_index)

    return True


def delete_questions(question_indexes):
    indexes = question_indexes.copy()
    indexes = sorted(indexes, reverse=True)

    for index in indexes:
        delete_question(index)
        questions_to_be_deleted().remove(index)


def hash_question(question_text):
    return hashlib.md5(question_text.encode('utf-8')).hexdigest()


st.title("Live anonymous questions suggestions")

st.header("Add Question")

with st.form(key="new_question"):
    new_question = st.text_area("Suggest a new question")
    to_add_question = st.form_submit_button("Add question")

    if to_add_question:
        add_question(new_question)
question_board_header = st.beta_container()
st.header("Question board")
hash_table = set()  # Instead of hash table, we should have done a queue as per a consumer producer pattern
upvote_charts = {}
while True:

    new_questions = []
    new_initial_upvotes = []
    new_indexes = []
    new_data = False

    # Get new questions added
    print("Searching new questions")
    for question_index, question_hash in enumerate(questions_hash_list()):
        if question_hash not in hash_table:
            new_data = True
            new_questions.append(questions_list()[question_index])
            new_initial_upvotes.append(questions_votes()[question_index])
            hash_table.add(question_hash)
            new_indexes.append(question_index)

    # Add elements for each new question added
    if new_data:
        print("Adding latest questions")
        for q_i, question, upvotes in zip(new_indexes, new_questions, new_initial_upvotes):
            question_container, question_vote = st.beta_columns(2)
            question_container.subheader(f"Question No: {q_i + 1}")
            upvote_charts[q_i] = question_vote.empty()
            upvote_charts[q_i].subheader(f"Upvotes: {upvotes}")
            question_container.write(question)
            to_vote = question_vote.button("Upvote", key=f"{q_i}vote", )

            if to_vote:
                vote_question(q_i, question_board_header)
    # Updates votes
    print("Updating vote counts")
    for q_i, upvote_chart in upvote_charts.items():
        latest_votes = questions_votes()
        upvote_chart.subheader(f"Upvotes: {latest_votes[q_i]}")

    time.sleep(1)
