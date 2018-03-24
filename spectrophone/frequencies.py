_PITCH_CLASS_0 = 261.63
_PITCH_CLASS_1 = 277.16
_PITCH_CLASS_2 = 293.67
_PITCH_CLASS_3 = 311.16
_PITCH_CLASS_4 = 329.63
_PITCH_CLASS_5 = 349.23
_PITCH_CLASS_6 = 370
_PITCH_CLASS_7 = 392
_PITCH_CLASS_8 = 415.31
_PITCH_CLASS_9 = 440
_PITCH_CLASS_10 = 466.16
_PITCH_CLASS_11 = 493.88


frequencies = {
    0: _PITCH_CLASS_0,
    'c': _PITCH_CLASS_0,

    1: _PITCH_CLASS_1,
    'c#': _PITCH_CLASS_1,
    'db': _PITCH_CLASS_1,

    2: _PITCH_CLASS_2,
    'd': _PITCH_CLASS_2,

    3: _PITCH_CLASS_3,
    'd#': _PITCH_CLASS_3,
    'eb': _PITCH_CLASS_3,

    4: _PITCH_CLASS_4,
    'e': _PITCH_CLASS_4,

    5: _PITCH_CLASS_5,
    'f': _PITCH_CLASS_5,

    6: _PITCH_CLASS_6,
    'f#': _PITCH_CLASS_6,
    'gb': _PITCH_CLASS_6,

    7: _PITCH_CLASS_7,
    'g': _PITCH_CLASS_7,

    8: _PITCH_CLASS_8,
    'g#': _PITCH_CLASS_8,
    'ab': _PITCH_CLASS_8,

    9: _PITCH_CLASS_9,
    'a': _PITCH_CLASS_9,

    10: _PITCH_CLASS_10,
    'a#': _PITCH_CLASS_10,
    'bb': _PITCH_CLASS_10,

    11: _PITCH_CLASS_11,
    'b': _PITCH_CLASS_11
}

for key in list(frequencies):
    if isinstance(key, str) and '#' in key:
        frequencies[key.replace('#', 's')] = frequencies[key]

for key in list(frequencies):
    if isinstance(key, str):
        frequencies[key.upper()] = frequencies[key]
