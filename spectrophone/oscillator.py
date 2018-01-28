import numpy as np
from warnings import warn

from spectrophone import config


class Oscillator:

    periods = {}

    __slots__ = (
        'frequency',
        'last_sample_i',
        'period',
        'last_amplitude'
    )

    def __init__(self, frequency):

        if frequency > config.max_freq:
            warn(f'frequency {frequency} exceeds max of {config.max_freq} hz,'
                 ' using {config.max_freq} instead.')
            frequency = config.max_freq

        self.frequency = frequency
        self.last_sample_i = 0
        self.last_amplitude = 0

        period_len = round(config.sample_rate / self.frequency)

        if (self.frequency, config.sample_rate) in Oscillator.periods:
            self.period = Oscillator.periods[self.frequency]
        else:
            self.period = (
                np.sin(np.arange(period_len)
                       * (self.frequency
                          * ((np.pi * 2) / config.sample_rate)))) * 32767
            Oscillator.periods[self.frequency] = self.period

    def get_samples(self, num, amplitude):
        """Assumes `num > 2 * len(self.period)`"""
        if amplitude <= config.silence_threshold:
            if self.last_amplitude > config.silence_threshold:
                last_period_tail = (self.period[self.last_sample_i:]
                                    * self.last_amplitude)
                samples = np.concatenate([
                    last_period_tail,
                    np.zeros(num - len(last_period_tail))
                ])
                self.last_amplitude = amplitude
                self.last_sample_i = 0
                return samples
            else:
                return None
        last_period_tail = (self.period[self.last_sample_i:]
                            * self.last_amplitude)
        self.last_amplitude = amplitude
        tile_count = (num - len(last_period_tail)) // len(self.period)
        chunk_tail_len = (num
                          - (tile_count * len(self.period))
                          - len(last_period_tail))
        self.last_sample_i = chunk_tail_len
        return np.concatenate([
            last_period_tail,
            np.tile(self.period * amplitude, tile_count),
            self.period[:chunk_tail_len] * amplitude
        ])
