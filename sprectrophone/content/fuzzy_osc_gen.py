from tqdm import tqdm
from blur import rand

from spectrophone.oscillator import Oscillator


def generate(num, pitch_weights, detune_weights,
             octave_weights):
    oscillators = []
    for i in tqdm(range(num), 'generating oscillators'):
        base_freq = rand.weighted_choice(pitch_weights)
        detuned_freq = base_freq + rand.pos_or_neg(
            rand.weighted_rand(detune_weights))
        freq = round(detuned_freq * rand.weighted_choice(octave_weights), 1)
        oscillators.append(Oscillator(freq))
    return sorted(oscillators, key=lambda o: o.frequency)
