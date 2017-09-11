import wave
import struct

import numpy

import config
from oscillator import Oscillator
from voice import Voice
from keyframe import Keyframe
import rendering


oscillator = Oscillator(440)

voices = [
    Voice(Oscillator(440))
]

voices[0].keyframes.extend([
    Keyframe(0, 0),
    Keyframe(1, 1)
])

samples = rendering.render(voices)
print(len(samples))
print(samples.shape)
print(samples.dtype)

with wave.open('out.wav', 'wb') as out:
    out.setparams(config.wave_params)
    out.writeframes(samples)
