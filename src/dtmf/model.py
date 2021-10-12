# pylint: disable=too-few-public-methods

"""
Object model for representing a dial string and the structure of its constituent pattern strings.
"""

from typing import Sequence


class Element:
    """
    Base class for elements of a DTMF string.
    """


class Tone(Element):
    """
    Represents a single DTMF tone.
    """

    def __init__(self, symbol: str):
        self._symbol = symbol

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.symbol == other.symbol
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._symbol!r})"

    def __str__(self) -> str:
        return self._symbol

    @property
    def symbol(self) -> str:
        """
        Gets the DTMF symbol that corresponds to this tone.
        """

        return self._symbol


class Pause(Element):
    """
    Represents a pause in DTMF signalling, heard as silence.
    """

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return ","


class String:
    """
    Series of DTMF tones and/or pauses.
    """

    def __init__(self, elements: Sequence[Element]):
        self._elements = list(elements)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.elements == other.elements
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._elements!r})"

    def __str__(self) -> str:
        return ''.join(map(str, self._elements))

    @property
    def elements(self) -> Sequence[Element]:
        """
        Gets the sequence of elements for this DTMF string.
        """

        return self._elements
