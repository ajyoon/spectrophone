from spectrophone import rendering
from spectrophone import osc_interpreter
from spectrophone import sampler_interpreter
from spectrophone import terminal
from spectrophone import writer
from content import the_transistorized_radio as content


out_path = 'out.wav'

sampler_voices = sampler_interpreter.interpret(content.score, content.samplers)
osc_voices = osc_interpreter.interpret(content.score, content.oscillators)
samples = rendering.render(osc_voices, sampler_voices)

writer.write('out.wav', samples)

terminal.bell()
print(f'drone machine finished successfully. data written to {out_path}')
