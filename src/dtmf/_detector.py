# pylint: disable=missing-module-docstring

from math import cos
from math import exp
from math import pi
from typing import Callable
from typing import Iterable
from typing import NamedTuple
from typing import Tuple

from ._info import freqs
from ._info import lookup_symbol
from .model import Tone


BLOCK_SIZE = 205


class DtmfBlockResult(NamedTuple):
    """
    Result of scanning an individual block of audio for DTMF tones from a larger buffer.
    """

    start: int
    """
    Starting position of the block, as a sample offset from the original audio buffer
    (zero-indexed). Can be used in slice notation.
    """

    end: int
    """
    (Ending position + 1) of the block, as a sample offset from the original audio buffer
    (zero-indexed). Can be used in slice notation.
    """

    tone: Tone
    """
    DTMF tone detected in the block, or None if no tone was detected.
    """


def detect(
    samples: Iterable[float],
    sample_rate: float,
    detect_threshold: float = None
) -> Iterable[DtmfBlockResult]:
    """
    Detect the presence of DTMF tones in a sequence of audio samples.
    """

    freq_filters = [(f, _goertzel(BLOCK_SIZE, sample_rate, f)) for f in freqs()]

    for block, start, end in _blocks(samples):
        sum_energy = sum((pow(abs(s), 2) for s in block))
        avg_energy = sum_energy / len(block)

        freq_mags = []
        for freq, filter_mag in freq_filters:
            mag_squared = pow(abs(filter_mag(block)), 2)
            norm_mag = mag_squared / sum_energy

            freq_mags.append((freq, norm_mag))

        detected_freqs = [f for f, m in freq_mags if m > (detect_threshold or avg_energy)]
        symbol = lookup_symbol(detected_freqs)
        if not symbol:
            yield DtmfBlockResult(start, end, None)
        else:
            yield DtmfBlockResult(start, end, Tone(symbol))


def _blocks(samples: Iterable[float]) -> Iterable[Tuple[int, int, Iterable[float]]]:
    block_start = 0
    while True:
        block = samples[block_start:block_start + BLOCK_SIZE]
        block_end = block_start + len(block)

        yield (block, block_start, block_end)
        if len(block) < BLOCK_SIZE:
            break

        block_start = block_end


def _goertzel(
    block_size: int,
    sample_rate: float,
    freq: float
) -> Callable[[Iterable[float]], float]:
    """
    Goertzel algorithm info:
    https://www.ti.com/lit/an/spra066/spra066.pdf
    """

    k = round(block_size * (freq / sample_rate))
    omega = (2 * pi * k) / block_size
    cos_omega = 2 * cos(omega)

    def _filter(samples: Iterable[float]) -> float:
        s_0 = 0
        s_1 = 0
        s_2 = 0
        for x_n in samples:
            s_0 = x_n + cos_omega * s_1 - s_2
            s_2 = s_1
            s_1 = s_0

        return s_0 - exp(-1.0 * omega) * s_1

    return  _filter
