from __future__ import annotations

from typing import List, Optional, Tuple

from recognizer.atn.transition import Transition


class ATNState:
    def __init__(self, id: int, *, is_skip: bool = False) -> None:
        from recognizer.atn.atn import ATN
        self.transitions: List[Tuple[ATNState, Transition]] = []
        self.id = id
        self.is_accept = False
        self.is_skip = is_skip
        self.atn: Optional[ATN] = None

    def add_transition(self, target: ATNState, e: Transition) -> None:
        self.transitions.append((target, e))

    def add_transitions(self, *args: Tuple[ATNState, Transition]) -> None:
        self.transitions.extend(args)

    def __str__(self) -> str:
        return f"{{{self.id}}}"


class BasicState(ATNState):
    ...


class AcceptState(ATNState):
    def __init__(self, id: int, token_type: int, *, is_skip: bool = False) -> None:
        super().__init__(id, is_skip=is_skip)
        self.is_accept = True
        self.token_type = token_type
