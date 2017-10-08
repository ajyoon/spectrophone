import os

from drone_machine import config
from drone_machine.sampler import Sampler
from drone_machine.frequencies import frequencies
from drone_machine.content import fuzzy_osc_gen
from drone_machine.score import Score


# Samplers ####################################################################

length_weights = [(w[0] * config.sample_rate, w[1]) for w in [
    # (seconds, weight)
    (0.01, 1),
    (0.05, 5),
    (0.1, 1),
    (0.5, 3),
    (1, 5),
    (10, 0)
]]

cage_amp_factor_weights = [
    (0.1, 20),
    (0.5, 4),
    (1, 1),
    (3, 0)
]

watts_amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 1),
    (3, 0)
]

samplers = [
    Sampler(
        source='cage_feldman.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=length_weights,
        amp_factor_weights=cage_amp_factor_weights
    ),
    Sampler(
        source='watts.wav',
        step=int(config.sample_rate // 10),
        event_prob_factor=1,
        length_weights=length_weights,
        amp_factor_weights=watts_amp_factor_weights
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
    (pitches['gf'], 8),
    (pitches['bf'], 5),
    (pitches['c'], 7),
    (pitches['df'], 3),
    (pitches['ef'], 1),
    (pitches['f'], 3),
]

detune_weights = [
    (0, 45),
    (1, 10),
    (2, 6),
    (20, 2),
    (50, 0),
]

# octave_weights = [
#     (1/8, 5),
#     (1/4, 15),
#     (1/2, 35),
#     (1, 20),
#     (2, 3),
#     (4, 0.5),
#     (8, 0.1),
# ]

octave_weights = [
    (1/8, 1),
    (1/4, 25),
    (1/2, 20),
    (1, 20),
    (2, 15),
    (4, 1),
    (8, 0.1),
]

oscillators = fuzzy_osc_gen.generate(
    num=1200,
    pitch_weights=pitch_weights,
    detune_weights=detune_weights,
    octave_weights=octave_weights
)


# Score #######################################################################

score_file_name = 'scorev2.png'
score_path = os.path.join(config.resources_dir, score_file_name)
score = Score(score_path)
