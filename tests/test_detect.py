import wave
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from dtmf import detect


def test_detect():
    def pcm_8_to_float(val: int) -> float:
        return -1.0 + val * (2.0 / 255)

    data = None
    sample_rate = None
    with wave.open("tests/dtmf_digits.wav") as wav_file:
        sample_rate = wav_file.getframerate()
        sample_count = wav_file.getnframes()
        data = list(map(pcm_8_to_float, wav_file.readframes(sample_count)))

    detect_threshold = None
    results = list(detect(data, sample_rate, detect_threshold=detect_threshold))

    _plot_results(data, sample_rate, detect_threshold, results)


def _plot_results(data: Iterable[float], sample_rate: float, detect_threshold: float, results: Iterable):
    big_n = len(data)
    t = big_n / sample_rate

    plt.axhline(0, color="blue")

    samples_x = np.linspace(0, t, big_n)
    samples_y = data
    plt.plot(samples_x, samples_y)
    plt.title(f"N={big_n}, t={t}s, threshold={detect_threshold or 'default'}")

    for result in results:
        if not result.tone:
            continue

        t_start = result.start / sample_rate
        t_end = result.end / sample_rate
        plt.axvspan(t_start, t_end, alpha=0.5, color="yellow")
        plt.text(t_start, -1, result.tone.symbol, verticalalignment="bottom")

    plt.show()
