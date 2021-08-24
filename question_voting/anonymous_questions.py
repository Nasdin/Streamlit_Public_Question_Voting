# import datetime
# import math
# from collections import deque
# from enum import Enum, unique
# from functools import partial
# from typing import List, Union
#
# import streamlit as st
#
# st.set_page_config("Anonymous questions voting")
# question_queue = deque()
#
#
#
#
#
# @st.cache(allow_output_mutation=True, persist=True)
# def shared_session_state() -> List:
#     """Shared state across all who come to this app"""
#     return []
#
#
# def add_new_question(question_text: str) -> bool:
#     new_question = Statement(question_text)
#     shared_session_state().append(new_question)
#     question_queue.append(new_question)
#     return True
#
#
# def add_comment_to_statement(
#         statement_index: int,
#         comment_text: str,
#         parent_shared_state: Union[List[Statement], Statement, None] = None) -> bool:
#     if parent_shared_state is None:
#         return add_comment_to_statement(statement_index, comment_text, shared_session_state())
#     elif isinstance(parent_shared_state, Statement):
#         return add_comment_to_statement(statement_index, comment_text, parent_shared_state.comments)
#
#     if isinstance(parent_shared_state, list):
#         new_comment = Statement(comment_text)
#         parent_shared_state[statement_index].add_comment(new_comment)
#         return True
#     raise ValueError("Not able to identify kind of object to add statements to")
#
#
# def add_upvote_to_statement(
#         statement_index: int,
#         parent_shared_state: Union[List[Statement], Statement, None] = None) -> bool:
#     if parent_shared_state is None:
#         return add_upvote_to_statement(statement_index, shared_session_state())
#     elif isinstance(parent_shared_state, Statement):
#         return add_upvote_to_statement(statement_index, parent_shared_state.comments)
#
#     if isinstance(parent_shared_state, list):
#         parent_shared_state[statement_index].upvote()
#         return True
#     raise ValueError("Not able to identify kind of object to add votes to")
#
#
# # % Utils %
# @unique
# class SecondsInTime(Enum):
#     minutes = 60
#     hour = 3600
#     day = 86400
#
#
# def time_delta_time_floored(seconds_in_time: SecondsInTime, timedelta: datetime.timedelta):
#     return math.floor(timedelta.seconds / seconds_in_time.value)
#
#
# time_delta_hours_floored = partial(time_delta_time_floored, SecondsInTime.hour)
# time_delta_minute_floored = partial(time_delta_time_floored, SecondsInTime.minute)
# time_delta_second_floored = partial(time_delta_time_floored, SecondsInTime.second)
#
#
# def time_delta_day_floored(timedelta: datetime.timedelta):
#     return timedelta.days
#
#
# def time_delta_month_floored(timedelta: datetime.timedelta):
#     return timedelta.days // 30
#
#
# def get_floored_timedelta_from_now(timestamp: datetime.datetime):
#     delta = datetime.datetime.now() - timestamp
#
#     do_hour = False
#     do_minute = False
#     do_seconds = False
#
#     hours = time_delta_hours_floored(delta)
#     if hours > 1:
#         pass
#
#
#
# def main():
#     pass
