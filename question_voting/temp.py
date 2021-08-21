# import hashlib
# import time
# import datetime
# from dataclasses import dataclass, field
# import uuid
#
# import streamlit as st
# from enum import Enum
# from collections import deque
# from operator import attrgetter
#
# from typing import List
#
# st.set_page_config("Anonymous questions voting")
#
#
# @st.cache(allow_output_mutation=True, persist=True)
# def questions_list():
#     return []
#
#
# @st.cache(allow_output_mutation=True, persist=True)
# def questions_hash_list():
#     return []
#
#
# @st.cache(allow_output_mutation=True, persist=True)
# def questions_votes():
#     return []
#
#
# @st.cache(allow_output_mutation=True, persist=True)
# def question_comments():
#     return {}
#
#
#
#
#
#
#
#
#
# def add_comments_to_question(question_text: str, comment: str):
#     question_hashed = hash_question(question_text)
#     comments_map = question_comments()
#     comments_map[question_hashed].append([comment, datetime.datetime.now(), 0])
#     st.info("Thanks for your comment")
#
#
# def add_question(question_text: str):
#     if question_text.strip() == "":
#         st.warning("Please add some texts")
#         return
#
#     question_hashed = hash_question(question_text)
#
#     if question_hashed in questions_hash_list():
#         st.warning("Question already added")
#         return
#     else:
#         q_l = questions_list()
#         q_v = questions_votes()
#         q_c = question_comments()
#         q_l.append(question_text)
#         q_v.append(0)
#         questions_hash_list().append(question_hashed)
#         q_c[question_hashed] = []
#         st.success("Your question has been added!")
#         return
#
#
# def vote_question(index_to_vote, header_container):
#     q_v = questions_votes()
#     q_v[index_to_vote] = q_v[index_to_vote] + 1
#     header_container.success("Thanks for voting")
#
#
# def hash_question(question_text):
#     return hashlib.md5(question_text.encode('utf-8')).hexdigest()
#
#
# def display_timedelta_from_now(timestamp):
#     delta = datetime.datetime.now() - timestamp
#     has_minutes = delta.seconds > 60
#     has_hour = delta.seconds > 3600
#     has_day = delta.seconds > 86400
#
#
# def display_comment(container, comment):
#     date_processed = datetime.datetime.now() - comment[1]
#     container.write(f"#### Anonymous commenter: {comment[1]}")
#     comment_box, to_upvote = st.beta_columns(2)
#     with container.beta_container():
#         comment_box.write(comment[0])
#     to_upvote.write(f"Upvotes: {comment[2]}")
#     return to_upvote.button("Upvote")
#
#
# def upvote_comment(comment):
#     comment[2] += 1
#     st.success("Thanks for upvoting the comment")
#
#
# def display_question_comments(container, question_text):
#     question_hashed = hash_question(question_text)
#     comments = question_comments()[question_hashed]
#
#     with container.beta_expander(f"See comments: {len(comments)} comments"):
#
#         container.subheader("Comments")
#         if len(comments) == 0:
#             container.write("There are no comments at the moment")
#         for comment in comments:
#             to_up_vote = display_comment(container, comment)
#             if to_up_vote:
#                 upvote_comment(comment)
#
#         add_comment_form(container, question_text)
#
#
# def add_comment_form(container, question_text):
#     with container.form(f"add_comment_{question_text}"):
#         comment = container.text_area(label="Add a public comment anonymously...",
#                                       key=f"add_comment_{question_text}_text")
#         _, _, right = container.beta_columns(3)
#         to_comment = right.form_submit_button("Comment")
#
#     if to_comment:
#         add_comments_to_question(question_text, comment)
#
#
# def main():
#
#
#
#
#         if to_add_question:
#             add_question(new_question)
#
#     question_board_header = st.beta_container()
#     st.header("Question board")
#     hash_table = set()  # Instead of hash table, we should have done a queue as per a consumer producer pattern
#     upvote_charts = {}
#     while True:
#
#         new_questions = []
#         new_initial_upvotes = []
#         new_indexes = []
#         new_data = False
#
#         # Get new questions added
#         print("Searching new questions")
#         for question_index, question_hash in enumerate(questions_hash_list()):
#             if question_hash not in hash_table:
#                 new_data = True
#                 new_questions.append(questions_list()[question_index])
#                 new_initial_upvotes.append(questions_votes()[question_index])
#                 hash_table.add(question_hash)
#                 new_indexes.append(question_index)
#
#         # Add elements for each new question added
#         if new_data:
#             print("Adding latest questions")
#             for q_i, question, upvotes in zip(new_indexes, new_questions, new_initial_upvotes):
#                 question_container, question_vote = st.beta_columns(2)
#                 # comment_container = st.beta_container()
#                 question_container.subheader(f"Question No: {q_i + 1}")
#                 upvote_charts[q_i] = question_vote.empty()
#                 upvote_charts[q_i].subheader(f"Upvotes: {upvotes}")
#
#                 question_container.write(question)
#                 to_vote = question_vote.button("Upvote", key=f"{q_i}vote", )
#                 display_question_comments(st, question)
#                 # add_comment_form(st, question)
#
#                 if to_vote:
#                     vote_question(q_i, question_board_header)
#         # Updates votes
#         print("Updating vote counts")
#         for q_i, upvote_chart in upvote_charts.items():
#             latest_votes = questions_votes()
#             upvote_chart.subheader(f"Upvotes: {latest_votes[q_i]}")
#
#         time.sleep(1)
#
#
# if __name__ == '__main__':
#     main()
