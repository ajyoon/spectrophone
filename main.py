import wave

import config
import rendering

import interpreter


samples = rendering.render(interpreter.voices)

with wave.open('out.wav', 'wb') as out:
    out.setparams(config.wave_params)
    out.writeframes(samples)
