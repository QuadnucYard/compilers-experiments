from typing import Optional
from recognizer.atn.atn import *
from recognizer.atn.atn_state import*
from recognizer.atn.transition import *
from recognizer.char_stream import CharStream
from recognizer.token import Token


class Lexer:

    def __init__(self, atn: ATN, input: CharStream) -> None:
        self.atn = atn
        self.input = input
        # self.token: Optional[Token] = None

    def next_token(self):
        s = self.atn.states[0]
        start_pos = self.input.pos
        c = self.input.peek()
        matched = True
        while matched:  # Token循环
            matched = False
            for ta, tr in s.transitions:
                if tr.matches(c):
                    s = ta
                    c = self.input.next()
                    matched = True
                    break
        if not isinstance(s, AcceptState):
            raise RuntimeError(f"Fail to accept. Last char is {chr(c)}({c}) at {self.input.pos}")
        elif not s.is_skip:
            return Token(self.input, s.token_type, start_pos, self.input.pos)
        return None

    def tokenize(self):
        while not self.input.end_of_stream():
            token = self.next_token()
            if token: yield token

