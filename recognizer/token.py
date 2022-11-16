

class Token:

    def __init__(self,source:"CharStream", type_: int, start:int, stop:int) -> None:
        self.source= source
        self.type_ =type_
        self.start= start
        self.stop = stop
        self.text = source.get_text(start, stop)

    def __str__(self) -> str:
        return f"[{self.start}:{self.stop}] {self.text} <{self.type_}>"

from recognizer.char_stream import CharStream