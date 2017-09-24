import numpy

from drone_machine import config


class Oscillator:

    periods = {}

    __slots__ = (
        'frequency',
        'last_sample_i',
        'period_samples',
        'last_amplitude'
    )

    def __init__(self, frequency):
        self.frequency = frequency
        self.last_sample_i = 0
        self.last_amplitude = 0

        period_len = round(config.sample_rate / self.frequency)

        if (self.frequency, config.sample_rate) in Oscillator.periods:
            self.period_samples = Oscillator.periods[self.frequency]
        else:
            self.period_samples = (
                numpy.sin(numpy.arange(period_len)
                          * (self.frequency
                             * ((numpy.pi * 2) / config.sample_rate)))) * 32767
            Oscillator.periods[self.frequency] = self.period_samples

    def get_samples(self, num, amplitude):
        """Assumes `num > 2 * len(self.period_samples)`"""
        last_period_tail = (self.period_samples[self.last_sample_i:]
                            * self.last_amplitude)
        self.last_amplitude = amplitude
        tile_count = (num - len(last_period_tail)) // len(self.period_samples)
        chunk_tail_len = (num
                          - (tile_count * len(self.period_samples))
                          - len(last_period_tail))
        self.last_sample_i = chunk_tail_len
        return numpy.concatenate([
            last_period_tail,
            numpy.tile(self.period_samples * amplitude, tile_count),
            self.period_samples[:chunk_tail_len] * amplitude
        ])
