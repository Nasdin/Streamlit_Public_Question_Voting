"""
Statements can be questions that can be commented upon, or they can also be comments that are also commentable
"""
import datetime
import uuid
from dataclasses import dataclass, field
from typing import List, Union

import streamlit as st

if "statements_built" not in st.session_state:
    st.session_state['statements_built'] = []


@dataclass
class Statement:
    """Class for keeping track of metadata regarding a single question or comment"""
    text: str
    votes: int = 0
    downvotes: int = 0
    comments: List['Comment'] = field(default_factory=list)
    hash: uuid.UUID = field(init=False)
    timestamp: datetime.datetime = field(init=False)

    statement_type: str = field(init=False)

    def __post_init__(self):
        self.hash = uuid.uuid4()
        self.timestamp = datetime.datetime.now()

    def add_comment(self, comment_key) -> None:
        """Adds a recursive Statement into this Statement as a comment which allows infinite nesting"""
        comment_text = st.session_state[comment_key]
        comment = Comment(comment_text)
        comment.parent = self.hash
        self.comments.append(comment)
        st.info("Your comment has been added")

    def upvote(self, session_key) -> None:
        if vote_key_swap(session_key):
            self.votes += 1
        else:
            self.votes -= 1

    def downvote(self, session_key) -> None:
        if vote_key_swap(session_key):
            self.downvotes += 1
        else:
            self.downvotes -= 1

    def comment_count(self) -> int:
        return len(self.comments)


@dataclass
class Question(Statement):
    """ A question posted by the admin"""
    statement_type: str = "Question"


@dataclass
class Comment(Statement):
    """ Like a statement, but a comment cannot be made for a comment. It also has to be tagged to a parent statement"""
    statement_type: str = "Comment"
    parent: str = field(init=False)


def vote_key_swap(key):
    if key not in st.session_state:
        st.session_state[key] = True
    elif st.session_state[key]:
        st.session_state[key] = False
    else:
        st.session_state[key] = True
    return st.session_state[key]


class DisplayStatement(object):

    def __init__(self,
                 container: st,
                 statement: Union[Question, Comment], ):
        self.container = container
        self.statement = statement
        self.comments_built = {}

        self.text_box = None
        self.to_upvote = None
        self.to_downvote = None
        self.upvote_count_box = None
        self.downvote_count_box = None
        self.comment_box = None

        self.upvote_key = None
        self.downvote_key = None

    def build_upvote(self):
        self.update_upvote()
        key = str(self.statement.hash) + "_upvote"
        if self.statement.statement_type == "Comment":
            key = key + str(self.statement.parent) + str(uuid.uuid4())
        self.upvote_key = key
        self.to_upvote.button("Upvote", on_click=self.statement.upvote, args=[key + "changer"], key=key,
                              help="Upvote if you agree")

    def update_upvote(self):
        self.upvote_count_box.write(f"Upvotes: {self.statement.votes}")

    def build_downvote(self):
        self.update_downvote()
        key = str(self.statement.hash) + "_downvote"
        if self.statement.statement_type == "Comment":
            key = key + str(self.statement.parent) + str(uuid.uuid4())
        self.downvote_key = key
        self.to_downvote.button("Downvote", on_click=self.statement.downvote, args=[key + "changer"], key=key,
                                help="Downvote if you think this is irrelevant")

    def update_downvote(self):
        self.downvote_count_box.write(f"Downvotes: {self.statement.downvotes}")

    def update_comments_section(self):

        comment_container = self.comment_box.container()
        with comment_container.expander(f"Total Comments: {self.statement.comment_count()}"):
            for comment in self.statement.comments:

                if comment.hash not in self.comments_built:
                    displayed_statement = DisplayStatement(st, comment)
                    self.comments_built[comment.hash] = displayed_statement
                else:
                    displayed_statement = self.comments_built[comment.hash]
                    # Needs to delete previously built so that we can build again
                    displayed_statement.unbuild()
                displayed_statement.build()
                displayed_statement.update()

    def build_comments_section(self):
        create_add_comments_form(self.container, self.statement)
        self.update_comments_section()

    def unbuild(self):
        del st.session_state[self.downvote_key]
        del st.session_state[self.upvote_key]
        del self.to_upvote
        del self.to_downvote
        del self.text_box
        del self.upvote_count_box
        del self.downvote_count_box
        del self.comment_box

    def init_build(self):
        self.container.write(f"### {self.statement.statement_type}: ")
        self.text_box, self.to_upvote, self.to_downvote = self.container.columns(3)

        self.upvote_count_box = self.to_upvote.empty()
        self.downvote_count_box = self.to_downvote.empty()
        self.comment_box = self.container.empty()

    def build(self):
        self.init_build()
        self.text_box.write(self.statement.text)
        self.build_upvote()
        self.build_downvote()

        if self.statement.statement_type == "Question":
            self.build_comments_section()

    def update(self):
        self.update_upvote()
        self.update_downvote()

        if self.statement.statement_type == "Question":
            self.update_comments_section()


def create_add_comments_form(container: st, parent_statement: Question):
    with container.form(key=f"add_question_form_{parent_statement.hash}"):
        st.subheader("Add a comment")
        st.text_area("Write your comment here", key=f"new_comment_text_{parent_statement.hash}")
        st.form_submit_button("Add comment",
                              help=f"Comment to be posted to this question",
                              on_click=parent_statement.add_comment,
                              kwargs={"comment_key": f"new_comment_text_{parent_statement.hash}"}
                              )
