# pylint: disable=missing-module-docstring

from typing import Iterable


_freqs = [
    697.0,
    770.0,
    852.0,
    941.0,
    1209.0,
    1336.0,
    1477.0,
    1633.0
]

_freq_map = {
    "1": [697.0, 1209.0],
    "2": [697.0, 1336.0],
    "3": [697.0, 1477.0],
    "A": [697.0, 1633.0],
    "4": [770.0, 1209.0],
    "5": [770.0, 1336.0],
    "6": [770.0, 1477.0],
    "B": [770.0, 1633.0],
    "7": [852.0, 1209.0],
    "8": [852.0, 1336.0],
    "9": [852.0, 1477.0],
    "C": [852.0, 1633.0],
    "*": [941.0, 1209.0],
    "0": [941.0, 1336.0],
    "#": [941.0, 1477.0],
    "D": [941.0, 1633.0]
}


def freqs() -> Iterable[float]:
    """
    Returns the list of distinct audio frequencies used in generating DTMF tones.
    """

    return _freqs


def lookup_freqs(symbol: str) -> Iterable[float]:
    """
    Lookup the pair of audio frequencies that correspond to a DTMF digit or symbol.
    """

    return _freq_map.get(symbol)


def lookup_symbol(tone_freqs: Iterable[float]) -> str:
    """
    Lookup the DTMF digit or symbol that corresponds to a list of distinct audio frequencies.
    """

    for symbol, symbol_freqs in _freq_map.items():
        if set(symbol_freqs) == set(tone_freqs):
            return symbol

    return None
