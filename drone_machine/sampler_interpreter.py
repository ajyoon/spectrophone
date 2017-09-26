import random

import numpy as np
from tqdm import tqdm
from blur import rand

from drone_machine import config
from drone_machine.sampler import Sampler
from drone_machine.sampler_voice import SamplerVoice
from drone_machine.sampler_event import SamplerEvent


length_weights = [(w[0] * config.sample_rate, w[1]) for w in [
    # (seconds, weight)
    (0.01, 1),
    (0.05, 5),
    (0.1, 1),
    (0.5, 3),
    (1, 1),
    (5, 0)
]]

fade_length = int(length_weights[0][0] / 3)

amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 1),
    (3, 0)
]


def interpret(score):
    sampler = Sampler(config.samples_paths['cage_feldman.wav'])
    sampler_voice = SamplerVoice(sampler)

    avg_map = np.average(score.amplitude_map, 0)

    for event_pos in tqdm(range(0, config.total_samples,
                                config.sampler_step),
                          'interpreting samplers'):
        x = int(event_pos / config.total_samples * len(avg_map))
        avg = avg_map[x]
        if rand.prob_bool(avg * config.sampler_event_prob_factor):
            length = min(int(rand.weighted_rand(length_weights)),
                         config.total_samples - event_pos)
            sample_pos = random.randint(0, len(sampler.samples) - length - 1)
            amp = avg * rand.weighted_rand(amp_factor_weights)
            sampler_voice.events.append(
                SamplerEvent(event_pos,
                             sample_pos,
                             length,
                             amp,
                             fade_length,
                             fade_length)
            )
    return sampler_voice
