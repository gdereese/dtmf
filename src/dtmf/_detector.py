# pylint: disable=missing-module-docstring

from typing import Iterable
from typing import NamedTuple
from typing import Tuple

from ._analysis import analyze
from ._analysis import AudioStats
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

    stats: AudioStats
    """
    Audio statistics for the block calculated during analysis.
    """


def detect(
    samples: Iterable[float],
    sample_rate: float,
    detect_threshold: float = None
) -> Iterable[DtmfBlockResult]:
    """
    Detect the presence of DTMF tones in a sequence of audio samples.
    """

    for block, start, end in _blocks(samples):
        stats = analyze(block, sample_rate)

        detected_freqs = (
            f
            for f, m
            in stats.freq_mags
            if m > (detect_threshold or stats.avg_energy)
        )

        symbol = lookup_symbol(list(detected_freqs))
        if not symbol:
            yield DtmfBlockResult(start, end, None, stats)
        else:
            yield DtmfBlockResult(start, end, Tone(symbol), stats)


def _blocks(samples: Iterable[float]) -> Iterable[Tuple[int, int, Iterable[float]]]:
    block_start = 0
    while True:
        block = samples[block_start:block_start + BLOCK_SIZE]
        block_end = block_start + len(block)

        yield (block, block_start, block_end)
        if len(block) < BLOCK_SIZE:
            break

        block_start = block_end
