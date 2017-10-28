import os

from spectrophone import config
from spectrophone.sampler import Sampler
from spectrophone.frequencies import frequencies
from content import fuzzy_osc_gen
from spectrophone.score import Score


num_osc = 6000
amp_multiplier = num_osc / 300


# Samplers ####################################################################

def weight_seconds_to_samples(weights):
    return [(w[0] * config.sample_rate, w[1]) for w in weights]


def apply_amp_weight_multiplier(weights):
    return [(w[0] * amp_multiplier, w[1]) for w in weights]


med_length_weights = weight_seconds_to_samples([
    # (seconds, weight)
    (0.01, 1),
    (0.05, 5),
    (0.1, 1),
    (0.5, 3),
    (1, 5),
    (10, 0)
])

long_length_weights = weight_seconds_to_samples([
    (0.01, 1),
    (0.05, 5),
    (0.1, 1),
    (0.5, 3),
    (1, 5),
    (80, 0)
])

low_amp_factor_weights = apply_amp_weight_multiplier([
    (0.005, 50),
    (0.3, 2),
    (1, 0.2),
    (3, 0)
])

med_amp_factor_weights = apply_amp_weight_multiplier([
    (0.1, 50),
    (0.5, 3),
    (1, 4),
    (3, 0)
])

loud_amp_factor_weights = apply_amp_weight_multiplier([
    (0.1, 13),
    (0.5, 4),
    (1, 3),
    (15, 0)
])

samplers = [
    Sampler(
        source='cage_feldman.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=med_length_weights,
        amp_factor_weights=med_amp_factor_weights
    ),
    Sampler(
        source='watts.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=0.7,
        length_weights=med_length_weights,
        amp_factor_weights=low_amp_factor_weights
    ),
    Sampler(
        source='oliveros.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1.3,
        length_weights=med_length_weights,
        amp_factor_weights=loud_amp_factor_weights
    ),
    Sampler(
        source='organ_1.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=long_length_weights,
        amp_factor_weights=med_amp_factor_weights
    ),
    Sampler(
        source='keys.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1.1,
        length_weights=med_length_weights,
        amp_factor_weights=loud_amp_factor_weights
    ),
    Sampler(
        source='singing.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1.5,
        length_weights=long_length_weights,
        amp_factor_weights=loud_amp_factor_weights
    ),
    Sampler(
        source='cooking.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1.5,
        length_weights=long_length_weights,
        amp_factor_weights=loud_amp_factor_weights
    ),
]

# Oscillators #################################################################

pitches = {
    'gf': frequencies[6],
    'bf': frequencies[10],
    'c': frequencies[0] * 2,
    'df': frequencies[1] * 2,
    'ef': frequencies[3] * 2,
    'f': frequencies[5] * 2
}

pitch_weights = [
    (pitches['gf'], 9),
    (pitches['bf'], 5),
    (pitches['c'], 7),
    (pitches['df'], 8),
    (pitches['ef'], 3),
    (pitches['f'], 5),
]

detune_weights = [
    (0, 45),
    (1, 10),
    (2, 6),
    (20, 2),
    (50, 0),
]

octave_weights = [
    (1/8, 4),
    (1/4, 25),
    (1/2, 20),
    (1, 20),
    (2, 15),
    (4, 1),
    (8, 0.1),
    (16, 0.001),
]

oscillators = fuzzy_osc_gen.generate(
    num=num_osc,
    pitch_weights=pitch_weights,
    detune_weights=detune_weights,
    octave_weights=octave_weights
)


# Score #######################################################################

score_file_name = 'the_transistorized_radio.png'
score_path = os.path.join(config.resources_dir, score_file_name)
score = Score(score_path)
