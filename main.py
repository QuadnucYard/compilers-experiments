from recognizer.lexer import Lexer
from recognizer.char_stream import CharStream
from myutils import *


def test(prog: CharStream):
    lex = Lexer(atn, prog)
    for t in lex.tokenize():
        if t.type_ == TokenType.ID.value and t.text in keywords:
            t.type_ = TokenType.KW.value
        print(f"{t.text} <{TokenType(t.type_).name}> [{t.start}:{t.stop}]")


tokenize_file("example1.c")
tokenize_file("example2.cpp")
tokenize_file("example3.cpp")
tokenize_file("example4.cpp")