import wave

import config
import rendering

import interpreter
#import content


samples = rendering.render_master(interpreter.voices)

with wave.open('out.wav', 'wb') as out:
    out.setparams(config.wave_params)
    out.writeframes(samples)
