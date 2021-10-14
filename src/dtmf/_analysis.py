# pylint: disable=missing-module-docstring

from math import cos
from math import exp
from math import pi

from typing import Callable
from typing import Iterable
from typing import NamedTuple
from typing import Tuple

from ._info import freqs


class AudioStats(NamedTuple):
    """
    Statistics generated during the analysis of a block of audio samples that are relevant
    to frequency detection.
    """

    sum_energy: float
    """
    Total sound energy detected in the audio block. This is calculated as the sum of the
    squared absolute value of each sample value.

    i.e. `sum(abs(x_n) ** 2)`
    """

    avg_energy: float
    """
    Average sound energy detected in the audio block. This is calculated by dividing the
    block's total energy by the number of samples in the block.

    i.e. `sum(abs(x_n) ** 2) / N`
    """

    freq_mags: Iterable[Tuple[float, float]]
    """
    List of audio frequencies included in the analysis, along with their measured magnitude
    expressed as the squared absolute value of the raw magnitude output by a Goertzel filter.
    """


def analyze(block: Iterable[float], sample_rate: float) -> AudioStats:
    """
    Performs a Goertzel frequency analysis on a block of audio samples.
    """

    block_size = len(block)
    freq_filters = [(f, _goertzel(block_size, sample_rate, f)) for f in freqs()]

    sum_energy = sum((pow(abs(s), 2) for s in block))
    avg_energy = sum_energy / block_size

    mags_squared = ((f, pow(abs(filter_func(block)), 2)) for f, filter_func in freq_filters)
    norm_mags = ((f, m / sum_energy) for f, m in mags_squared)

    return AudioStats(sum_energy, avg_energy, list(norm_mags))


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
