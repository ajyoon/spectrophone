import os

from spectrophone import config
from spectrophone.sampler import Sampler
from spectrophone.frequencies import frequencies
from content import fuzzy_osc_gen
from spectrophone.score import Score


# Samplers ####################################################################

def weight_seconds_to_samples(weights):
    return [(w[0] * config.sample_rate, w[1]) for w in weights]


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

cage_feldman_amp_factor_weights = [
    (0.1, 20),
    (0.5, 4),
    (1, 3),
    (5, 0)
]

watts_amp_factor_weights = [
    (0.01, 50),
    (0.3, 3),
    (1, 1),
    (3, 0)
]

oliveros_amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 4),
    (5, 0)
]

organ_1_amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 4),
    (7, 0)
]

organ_2_amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 4),
    (7, 0)
]

keys_amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 4),
    (3, 0)
]

singing_amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 4),
    (3, 0)
]

cooking_amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 4),
    (3, 0)
]

samplers = [
    Sampler(
        source='cage_feldman.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=med_length_weights,
        amp_factor_weights=cage_feldman_amp_factor_weights
    ),
    Sampler(
        source='watts.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=med_length_weights,
        amp_factor_weights=watts_amp_factor_weights
    ),
    Sampler(
        source='oliveros.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=med_length_weights,
        amp_factor_weights=oliveros_amp_factor_weights
    ),
    Sampler(
        source='organ_1.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=long_length_weights,
        amp_factor_weights=organ_1_amp_factor_weights
    ),
    Sampler(
        source='organ_2.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=long_length_weights,
        amp_factor_weights=organ_2_amp_factor_weights
    ),
    Sampler(
        source='keys.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=med_length_weights,
        amp_factor_weights=keys_amp_factor_weights
    ),
    Sampler(
        source='cooking.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=med_length_weights,
        amp_factor_weights=cooking_amp_factor_weights
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
]

oscillators = fuzzy_osc_gen.generate(
    num=2000,
    pitch_weights=pitch_weights,
    detune_weights=detune_weights,
    octave_weights=octave_weights
)


# Score #######################################################################

score_file_name = 'scorev2.png'
score_path = os.path.join(config.resources_dir, score_file_name)
score = Score(score_path)
