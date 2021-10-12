# pylint: disable=missing-module-docstring

from functools import lru_cache
from itertools import chain
from itertools import cycle
from itertools import islice
from math import ceil
from math import pi
from math import sin
from typing import Iterable

from ._info import lookup_freqs
from .model import Pause
from .model import Tone
from .model import String
from .model import Element


def generate(
    string: String,
    level: float = 0,
    mark_duration: float = 0.04,
    space_duration: float = 0.04,
    pause_duration: float = 1,
    sample_rate: int = 8000
) -> Iterable[float]:
    """
    Generate audio for a string of DTMF tones and/or pauses.
    """

    tones = (
        _element(el, level, mark_duration, space_duration, pause_duration, sample_rate)
        for el
        in string.elements
    )

    return chain(*tones)


def _element(
    element: Element,
    level: float,
    mark_duration: float,
    space_duration: float,
    pause_duration: float,
    sample_rate: int
) -> Iterable[float]:
    if isinstance(element, Pause):
        return _pause(pause_duration, sample_rate)
    if isinstance(element, Tone):
        return _tone(element, level, mark_duration, space_duration, sample_rate)


def _pause(duration: float, sample_rate: int):
    return _trim(_silence(), duration, sample_rate)


def _tone(
    tone: Tone,
    level: float,
    mark_duration: float,
    space_duration: float,
    sample_rate: int
) -> Iterable[float]:
    freqs = lookup_freqs(tone.symbol)
    comps = (cycle(_sine_wave(f, level, sample_rate)) for f in freqs)
    tone = map(sum, zip(*comps))

    mark_sample_count = ceil(mark_duration * sample_rate)
    mark_gen = islice(tone, mark_sample_count)

    space_sample_count = ceil(space_duration * sample_rate)
    space_gen = islice(_silence(), space_sample_count)

    return chain(mark_gen, space_gen)


def _trim(gen: Iterable[float], duration: float, sample_rate: int) -> Iterable[float]:
    sample_count = ceil(duration * sample_rate)

    return islice(gen, sample_count)


def _silence() -> Iterable[float]:
    return cycle((0,))


@lru_cache
def _sine_wave(frequency: int, level: float, sample_rate: int) -> Iterable[float]:
    # convert level in dBm (decibel-millivolt) to amplitude/power in mW (milliwatt)
    #   mW = 10 ^ (dBm / 10)
    # 1 mW = 0 dBm
    amplitude = 10 ** (level / 10)

    period = ceil(sample_rate / frequency)

    return [
        amplitude * sin(2 * pi * frequency * ((x % period) / sample_rate))
        for x
        in range(period)
    ]
