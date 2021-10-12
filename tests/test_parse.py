from dtmf import parse
from dtmf.model import Pause
from dtmf.model import String
from dtmf.model import Tone


def test_parse():
    input = "5551234,,500#"

    string = parse(input)

    assert string == String([
        Tone("5"),
        Tone("5"),
        Tone("5"),
        Tone("1"),
        Tone("2"),
        Tone("3"),
        Tone("4"),
        Pause(),
        Pause(),
        Tone("5"),
        Tone("0"),
        Tone("0"),
        Tone("#"),
    ])
