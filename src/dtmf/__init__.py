"""
Package for working with DTMF - a system for signaling over the voice band of a telephony system
using multi-frequency tones.
"""

from ._detector import detect
from ._generator import generate
from ._parser import parse

__all__ = [
    detect.__name__,
    generate.__name__,
    parse.__name__,
]
