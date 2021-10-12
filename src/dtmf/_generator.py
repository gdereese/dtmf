# pylint: disable=missing-module-docstring

from functools import lru_cache
from itertools import chain
from itertools import cycle
from itertools import islice
from math import ceil
from math import pi
from math import sin
from typing import Iterable
from typing import NamedTuple

from ._info import lookup_freqs
from .model import Pause
from .model import Tone

from .model import String
from .model import Element


class GenerationParams(NamedTuple):
    """
    Parameters for the audio generation of DTMF tones.
    """

    level: float = 0
    """
    Audio level of the tones, in dBm (decibel-millivolts).
    """

    mark_duration: float = 0.04
    """
    Duration that each DTMF tone sounds, in seconds.
    """

    space_duration: float = 0.04
    """
    Duration of silence between consecutive DTMF tones, in seconds.
    """

    pause_duration: float = 1.0
    """
    Duration of silence to use for pauses, in seconds.
    """


def generate(
    string: String,
    params: GenerationParams = None,
    sample_rate: int = 8000
) -> Iterable[float]:
    """
    Generate audio for a string of DTMF tones and/or pauses.
    """
    params = params or GenerationParams()

    tones = (
        _element(el, params, sample_rate)
        for el
        in string.elements
    )

    return chain(*tones)


def _element(
    element: Element,
    params: GenerationParams,
    sample_rate: int
) -> Iterable[float]:
    if isinstance(element, Pause):
        return _pause(params.pause_duration, sample_rate)
    if isinstance(element, Tone):
        return _tone(
            element,
            params.level,
            params.mark_duration,
            params.space_duration,
            sample_rate
        )

    raise ValueError(f"unrecognized element type: {element.__class__.__name__}")


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
