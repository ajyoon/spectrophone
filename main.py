import wave

import config
import rendering

import content

samples = rendering.render(content.voices)

with wave.open('out.wav', 'wb') as out:
    out.setparams(config.wave_params)
    out.writeframes(samples)
