import os

import numpy as np

from spectrophone import config


class Sampler:

    """A sound sampler for a .wav audio file.

    Assumes the file is mono-channel and encoded in signed 16-bit integers.
    """

    def __init__(self, source, step, event_prob_factor, length_weights,
                 amp_factor_weights):
        self.source = source
        self.step = step
        self.event_prob_factor = event_prob_factor
        self.length_weights = length_weights
        self.amp_factor_weights = amp_factor_weights
        self.samples = Sampler._load_samples(self._abs_source_path)

    def get_samples(self, pos, length, amp, fade_in_len, fade_out_len):
        samples = self.samples[pos:pos + length].astype(np.float64)
        samples[:fade_in_len] *= Sampler._fade_in_ramp(fade_in_len, amp)
        samples[-fade_in_len:] *= Sampler._fade_out_ramp(fade_out_len, amp)
        return samples

    @property
    def fade_length(self):
        return int(self.length_weights[0][0] / 3)

    @property
    def _abs_source_path(self):
        return os.path.join(config.resources_dir, self.source)

    @staticmethod
    def _fade_in_ramp(length, end_amp):
        slope = end_amp / length
        array = np.ndarray(length)
        for i in range(len(array)):
            array[i] = i * slope
        return array

    @staticmethod
    def _fade_out_ramp(length, start_amp):
        return Sampler._fade_in_ramp(length, start_amp)[::-1]

    @staticmethod
    def _load_samples(source_path):
        return np.fromfile(open(source_path), np.int16)[24:]
