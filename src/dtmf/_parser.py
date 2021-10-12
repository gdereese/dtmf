# pylint: disable=missing-module-docstring

from typing import Iterable

from .model import Pause
from .model import String
from .model import Tone
from .model import Element


def parse(string: str) -> String:
    """
    Parses a dial string into an equivalent object representation.
    """

    elements = _parse_elements(string)

    return String(elements)


def _parse_elements(string: str) -> Iterable[Element]:
    pos = 0
    for char in string:
        if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "#", "*"]:
            yield Tone(char)
        elif char in [","]:
            yield Pause()
        else:
            raise ValueError("invalid DTMF char at position {pos}: '{char}'")

        pos += 1
