import wave

import numpy
from tqdm import tqdm

from drone_machine import config
from drone_machine import rendering
from drone_machine import osc_interpreter
from drone_machine import sampler_interpreter
from drone_machine import terminal
from drone_machine.score import Score
from drone_machine.content import test


out_path = 'out.wav'

score = Score(config.score_path)

osc_voices = osc_interpreter.interpret(score, test.oscillators)
sampler_voices = sampler_interpreter.interpret(score, test.samplers)
samples = rendering.render(osc_voices, sampler_voices)

with wave.open(out_path, 'wb') as out:
    print(f'writing audio data to {out_path}')
    out.setparams(config.wave_params)
    write_chunks = numpy.array_split(samples,
                                     len(samples) // config.sample_rate)
    for write_chunk in tqdm(write_chunks, f'writing to {out_path}'):
        out.writeframes(write_chunk)

terminal.bell()
print(f'drone machine finished successfully. data written to {out_path}')
