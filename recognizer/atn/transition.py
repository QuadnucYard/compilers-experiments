from abc import abstractmethod
from typing import Set


class Transition:
    @abstractmethod
    def matches(self, symbol: int) -> bool:
        ...


class AtomTransition(Transition):
    def __init__(self, label: int) -> None:
        super().__init__()
        self.label = label

    def matches(self, symbol: int) -> bool:
        return symbol == self.label

    def __str__(self) -> str:
        return chr(self.label)


class SetTransition(Transition):
    def __init__(self, set_: Set[int]) -> None:
        super().__init__()
        self.set_ = set_

    def matches(self, symbol: int) -> bool:
        return symbol in self.set_

    @classmethod
    def create(cls, set_: str) -> "SetTransition":
        return SetTransition({ord(c) for c in set_})

    def __str__(self) -> str:
        return self.set_.__str__()


class RangeTransition(Transition):
    def __init__(self, from_: int, to_: int) -> None:
        super().__init__()
        self.from_ = from_
        self.to_ = to_

    def matches(self, symbol: int) -> bool:
        return self.from_ <= symbol <= self.to_

    def __str__(self) -> str:
        return f"'{self.from_}..{self.to_}'"
