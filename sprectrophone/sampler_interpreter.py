import random

import numpy as np
from tqdm import tqdm
from blur import rand

from spectrophone import config
from spectrophone.sampler_voice import SamplerVoice
from spectrophone.sampler_event import SamplerEvent


def interpret(score, samplers):
    avg_map = np.average(score.amplitude_map, 0)
    voices = []
    for sampler in tqdm(samplers, 'interpreting samplers'):
        voices.append(_interpret_sampler(sampler, avg_map))
    return voices


def _interpret_sampler(sampler, avg_map):
    sampler_voice = SamplerVoice(sampler)
    for event_pos in tqdm(range(0, config.total_samples,
                                sampler.step),
                          f'interpreting {sampler.source}'):
        x = int(event_pos / config.total_samples * len(avg_map))
        avg = avg_map[x] * sampler.event_prob_factor
        if rand.prob_bool(avg):
            length = min(int(rand.weighted_rand(sampler.length_weights)),
                         config.total_samples - event_pos)
            sample_pos = random.randint(0, len(sampler.samples) - length - 1)
            amp = avg * rand.weighted_rand(sampler.amp_factor_weights)
            sampler_voice.events.append(
                SamplerEvent(event_pos,
                             sample_pos,
                             length,
                             amp,
                             sampler.fade_length,
                             sampler.fade_length)
            )
    return sampler_voice
