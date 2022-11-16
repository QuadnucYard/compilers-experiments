from typing import List
from recognizer.atn.atn_state import ATNState


class ATN:
    def __init__(self) -> None:
        self.states: List[ATNState] = []

    def add_state(self, state: ATNState) -> None:
        state.atn = self
        self.states.append(state)

    def add_states(self, states: List[ATNState]):
        for s in states:
            self.add_state(s)