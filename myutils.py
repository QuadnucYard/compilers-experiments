from enum import Enum, auto
from pathlib import Path
import re
import string
from recognizer.atn.atn import *
from recognizer.atn.atn_state import AcceptState, BasicState
from recognizer.atn.transition import *
from recognizer.lexer import Lexer
from recognizer.char_stream import CharStream
from recognizer.token import Token


class TransitionFactory:
    @staticmethod
    def create(s: str) -> Transition:
        if len(s) == 1:
            return AtomTransition(ord(s))
        if m := re.match(r"\[(.+)(?<!\\)\-(.+)\]", s):
            return RangeTransition(ord(m.group(1)), ord(m.group(2)))
        if m := re.match(r"\[(.+)\]", s):
            return SetTransition.create(m.group(1))
        raise Exception("Unknown transition")


class TokenType(Enum):
    ID = auto()
    KW = auto()
    INT = auto()
    FLOAT = auto()
    CHAR = auto()
    STRING = auto()
    PUNC = auto()
    OP = auto()
    OTHER = auto()
    WS = auto()


keywords = {
    "auto",
    "bool",
    "break",
    "case",
    "char",
    "const",
    "constexpr",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "false",
    "float",
    "for",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "namespace",
    "nullptr",
    "register",
    "restrict",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "static_assert",
    "struct",
    "switch",
    "true",
    "typedef",
    "typeof",
    "union",
    "unsigned",
    "using",
    "void",
    "volatile",
    "while",
}


def create_lex_atn():

    atn = ATN()

    t_digit = TransitionFactory.create("[0-9]")
    t_non_digit = SetTransition.create(string.ascii_letters + "_")
    t_any_char = SetTransition.create(string.printable)

    # Start
    s0 = ATNState(0, is_skip=True)

    # Identifier
    s1 = AcceptState(1, TokenType.ID.value)
    s0.add_transition(s1, t_non_digit)
    s1.add_transitions((s1, t_digit), (s1, t_non_digit))

    # Integer & Float
    s11 = AcceptState(11, TokenType.INT.value)
    s12 = BasicState(12)
    s13 = AcceptState(13, TokenType.FLOAT.value)
    s14 = BasicState(14)
    s15 = BasicState(15)
    s16 = AcceptState(16, TokenType.FLOAT.value)
    s0.add_transition(s11, t_digit)
    s11.add_transitions((s11, t_digit), (s12, TransitionFactory.create(".")))
    s12.add_transition(s13, t_digit)
    s13.add_transitions((s13, t_digit), (s14, TransitionFactory.create("[eE]")))
    s14.add_transitions((s16, t_digit), (s15, TransitionFactory.create("[+-]")))
    s15.add_transition(s16, t_digit)
    s16.add_transition(s16, t_digit)

    # Character
    s21 = BasicState(21)
    s22 = BasicState(22)
    s23 = BasicState(23)
    s24 = AcceptState(24, TokenType.CHAR.value)
    s0.add_transition(s21, TransitionFactory.create("'"))
    s21.add_transitions((s22, TransitionFactory.create("\\")), (s23, t_any_char))
    s22.add_transition(s23, t_any_char)
    s23.add_transition(s24, TransitionFactory.create("'"))

    # String
    s31 = BasicState(31)
    s32 = BasicState(32)
    s33 = AcceptState(33, TokenType.STRING.value)
    s0.add_transition(s31, TransitionFactory.create("\""))
    s31.add_transitions(
        (s32, TransitionFactory.create("\\")),
        (s33, TransitionFactory.create("\"")),
        (s31, t_any_char),
    )
    s32.add_transition(s31, t_any_char)

    # Operator & Punctuator
    s101 = AcceptState(101, TokenType.OP.value)
    s102 = AcceptState(102, TokenType.OP.value)
    s103 = AcceptState(103, TokenType.OP.value)
    s104 = AcceptState(104, TokenType.OP.value)
    s105 = AcceptState(105, TokenType.OP.value)
    s106 = AcceptState(106, TokenType.OP.value)
    s107 = AcceptState(107, TokenType.OP.value)
    s108 = AcceptState(108, TokenType.OP.value)
    s109 = AcceptState(109, TokenType.OP.value)
    s110 = AcceptState(110, TokenType.OP.value)
    s111 = AcceptState(111, TokenType.OP.value)
    s112 = AcceptState(112, TokenType.OP.value)
    s113 = AcceptState(113, TokenType.OP.value)
    s114 = AcceptState(114, TokenType.OP.value)
    s115 = AcceptState(115, TokenType.PUNC.value)
    s0.add_transitions(
        (s101, TransitionFactory.create("=")),
        (s103, TransitionFactory.create("!")),
        (s105, TransitionFactory.create("<")),
        (s107, TransitionFactory.create(">")),
        (s109, TransitionFactory.create("&")),
        (s111, TransitionFactory.create("|")),
        (s113, SetTransition.create("+-*/%^&~")),
        (s114, SetTransition.create("!")),
        (s115, SetTransition.create("{}[]();:.,")),
    )
    s101.add_transition(s102, TransitionFactory.create("="))
    s103.add_transition(s104, TransitionFactory.create("="))
    s105.add_transition(s106, TransitionFactory.create("="))
    s107.add_transition(s108, TransitionFactory.create("="))
    s109.add_transition(s110, TransitionFactory.create("&"))
    s111.add_transition(s112, TransitionFactory.create("|"))

    # WS
    s5 = AcceptState(5, TokenType.WS.value, is_skip=True)
    s0.add_transition(s5, SetTransition.create(string.whitespace))

    atn.add_states([s0])

    return atn


atn = create_lex_atn()


def get_token_str(t: Token):
    return f"{t.text} <{TokenType(t.type_).name}> [{t.start}:{t.stop}]"


def tokenize_file(filename: str):
    prog = CharStream.from_path(f"sources/{filename}")
    lex = Lexer(atn, prog)
    tokens: List[Token] = []
    for t in lex.tokenize():
        if t.type_ == TokenType.ID.value and t.text in keywords:
            t.type_ = TokenType.KW.value
        tokens.append(t)
    Path(f"out/{Path(filename).stem}.txt").write_text("\n".join(get_token_str(t) for t in tokens))
    return tokens