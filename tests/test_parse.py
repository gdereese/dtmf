from dtmf import parse
from dtmf.model import DtmfPause
from dtmf.model import DtmfString
from dtmf.model import DtmfTone


def test_parse():
    input = "5551234,,500#"

    string = parse(input)

    assert string == DtmfString([
        DtmfTone("5"),
        DtmfTone("5"),
        DtmfTone("5"),
        DtmfTone("1"),
        DtmfTone("2"),
        DtmfTone("3"),
        DtmfTone("4"),
        DtmfPause(),
        DtmfPause(),
        DtmfTone("5"),
        DtmfTone("0"),
        DtmfTone("0"),
        DtmfTone("#"),
    ])
