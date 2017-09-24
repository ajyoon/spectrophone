import numpy

import config


class Oscillator:

    periods = {}

    __slots__ = (
        'frequency',
        'last_played_sample',
        'period_length',
        'period_samples',
        'last_amplitude'
    )

    def __init__(self, frequency):
        self.frequency = frequency
        self.last_played_sample = 0
        self.last_amplitude = 0

        self.period_length = round(config.sample_rate / self.frequency)

        if (self.frequency, config.sample_rate) in Oscillator.periods:
            self.period_samples = Oscillator.periods[self.frequency]
        else:
            self.period_samples = (
                numpy.sin(numpy.arange(self.period_length)
                          * (self.frequency
                             * ((numpy.pi * 2) / config.sample_rate)))) * 32767
            Oscillator.periods[self.frequency] = self.period_samples

    def get_samples(self, num, amplitude):
        if self.last_amplitude < config.silence_threshold < amplitude:
            self.last_played_sample = 0
        self.last_amplitude = amplitude
        rolled_array = numpy.concatenate([
            self.period_samples[self.last_played_sample:],
            self.period_samples[:self.last_played_sample]
        ])
        full_count, remainder = divmod(num, self.period_length)
        final_subarray = rolled_array[:remainder]
        return_array = numpy.concatenate((numpy.tile(rolled_array, full_count),
                                          final_subarray))

        self.last_played_sample = ((self.last_played_sample + remainder) %
                                   self.period_length)
        return return_array * amplitude
