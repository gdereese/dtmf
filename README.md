# dtmf

![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/gdereese/dtmf/CI/main?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/dtmf?style=for-the-badge)

Package for working with DTMF - a system for signaling over the voice band of a telephony system using multi-frequency tones.

## Features

* Parses dial strings (digits, symbols, etc.) into an object representation
* Constructs dial strings from element objects
* Detects the presence and position of DTMF tones in an audio buffer
* Generates DTMF audio from dial strings

## Installation

```shell
pip install dtmf
```

## What is DTMF?

Dual-tone multi-frequency signaling (DTMF) is a telecommunication signaling system used between telephone equipment and other communications devices. DTMF became known in the United States as 'Touch-Tone' for use in push-button telephones supplied to telephone customers.

DTMF tones use a mixture of two sine waves at different frequencies. Eight different audio frequencies are combined in pairs to make 16 unique tones. A tone is assigned to each of the digits from 0 to 9, the letters A to D, and the symbols # and *. The combination used for each tone are as follows:

|            | **1209 Hz** | **1336 Hz** | **1477 Hz** | **1633 Hz** |
| ---------- | :---------: | :---------: | :---------: | :---------: |
| **697 Hz** | 1           | 2           | 3           | A           |
| **770 Hz** | 4           | 5           | 6           | B           |
| **852 Hz** | 7           | 8           | 9           | C           |
| **941 Hz** | *           | 0           | #           | D           |

### Dial string syntax

A dial string is a textual representation of a sequence of DTMF digits and/or symbols. This format is commonly used as input to a telephone modem or another telephony device with automatic dialing as instructions for dialing the recipient of an outgoing call.

Dial strings use the following DTMF symbols:

* `0`-`9`
* `A`-`D`
* `*` or `E`
* `#` or `F`

In addition to the 16 DTMF symbols, dial strings support the following additional symbols:

* `P` or `,` for a momentary pause (usually 2 seconds)

## Usage

### Parsing a dial string

```python
from dtmf import parse

dial_str = "5551234,500#"

obj = parse(input)

print(repr(obj))
```

**Output:**

```text
String([
    Tone("5"),
    Tone("5"),
    Tone("5"),
    Tone("1"),
    Tone("2"),
    Tone("3"),
    Tone("4"),
    Pause(),
    Tone("5"),
    Tone("0"),
    Tone("0"),
    Tone("#")
])
```

### Constructing a dial string

```python
import dtmf.model as model

obj = model.String([
    model.Tone("5"),
    model.Tone("5"),
    model.Tone("5"),
    model.Tone("1"),
    model.Tone("2"),
    model.Tone("3"),
    model.Tone("4"),
    model.Pause(),
    model.Tone("5"),
    model.Tone("0"),
    model.Tone("0"),
    model.Tone("#")
])

print(str(obj))
```

**Output:**

```text
5551234,500#
```

### Detecting DTMF tones in an audio buffer

```python
from dtmf import detect

# list of audio samples as floats
data = [...]
sample_rate = 8000

results = detect(data, sample_rate)

for result in results:
    print(f"{result.start:<3d} - {result.end:>5d} : {result.tone!s}")
```

**Output:**

```text
  0 - 105 : 5
105 - 210 : 5
210 - 315 : 5
315 - 420 : 5
420 - 525 : None
...
```

### Generating DTMF audio from a dial string

```python
from dtmf import generate
import dtmf.model as model

obj = model.String([
    model.Tone("5"),
    model.Tone("5"),
    model.Tone("5"),
    model.Tone("1"),
    model.Tone("2"),
    model.Tone("3"),
    model.Tone("4"),
    model.Pause(),
    model.Tone("5"),
    model.Tone("0"),
    model.Tone("0"),
    model.Tone("#")
])

audio = generate(obj)
```

## Support

Please use the project's [Issues page](https://github.com/gdereese/dtmf/issues) to report any issues.

## Contributing

### Installing for development

```shell
poetry install
```

### Linting source files

```shell
poetry run pylint --rcfile .pylintrc src/dtmf
```

### Running tests

```shell
poetry run pytest
```

## License

This library is licensed under the terms of the [MIT](https://choosealicense.com/licenses/MIT/) license.
