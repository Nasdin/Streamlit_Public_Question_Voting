from collections import OrderedDict
from typing import Dict

import streamlit as st


class ViewMode(object):

    @staticmethod
    def mode():
        if "viewing_mode" not in st.session_state:
            st.session_state['viewing_mode'] = "VOTING"
        return st.session_state['viewing_mode']

    @staticmethod
    def reporting():
        st.session_state['viewing_mode'] = "REPORTING"

    @staticmethod
    def voting():
        st.session_state['viewing_mode'] = "VOTING"


class GlobalSharedStatements(object):

    def __init__(self, number):
        self.id = number

    @property
    def statements(self):
        return self._statements(self.id)

    @st.cache(persist=True,
              allow_output_mutation=True,
              show_spinner=False,
              suppress_st_warning=True)
    def _statements(self, x):
        return OrderedDict()

    def clear(self):
        for i in self.statements:
            self.statements.pop(i)
        st.sidebar.warning(f"You've cleared panel {self.id + 1}")


class GlobalPanels(object):
    dict_type = dict

    @classmethod
    @st.cache(persist=True,
              allow_output_mutation=True,
              show_spinner=False,
              suppress_st_warning=True)
    def _secret_stash(cls) -> Dict[int, GlobalSharedStatements]:
        return cls.dict_type()

    @classmethod
    def panels(cls):
        return cls._secret_stash()

    @classmethod
    def clear(cls):
        keys = cls._secret_stash().keys()
        for i in keys:
            cls._secret_stash().pop(i)
