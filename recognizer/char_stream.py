from pathlib import Path
from typing import Any


class CharStream:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0

    def peek(self) -> int:
        if self.pos == len(self.text):
            return -1
        return ord(self.text[self.pos])

    def next(self) -> int:
        self.pos += 1
        return self.peek()

    def end_of_stream(self) -> bool:
        return self.pos == len(self.text)

    def get_text(self, l: int, r: int):
        return self.text[l : r]

    @classmethod
    def from_path(cls, path: Any):
        return CharStream(Path(path).read_text(encoding="utf8"))

