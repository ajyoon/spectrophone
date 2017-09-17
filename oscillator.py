import numpy

import config


class Oscillator:

    periods = {}

    def __init__(self, frequency):
        self.frequency = frequency
        self.last_played_sample = 0

        self.period_length = round(config.framerate / self.frequency)

        if (self.frequency, config.framerate) in Oscillator.periods:
            self.period_samples = Oscillator.periods[self.frequency]
        else:
            self.period_samples = (
                numpy.sin(numpy.arange(self.period_length)
                          * (self.frequency
                             * ((numpy.pi * 2) / config.framerate)))) * 32767
            Oscillator.periods[self.frequency] = self.period_samples

    def get_samples(self, num, amplitude):
        if amplitude <= config.silence_threshold:
            return None

        rolled_array = numpy.roll(self.period_samples,
                                  -1 * self.last_played_sample)
        full_count, remainder = divmod(num, self.period_length)
        final_subarray = rolled_array[:remainder]
        return_array = numpy.concatenate((numpy.tile(rolled_array, full_count),
                                          final_subarray))

        self.last_played_sample = ((self.last_played_sample + remainder) %
                                   self.period_length)
        return return_array * amplitude
