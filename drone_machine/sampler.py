import numpy as np


class Sampler:

    """A sound sampler for a .wav audio file.

    Assumes the file is mono-channel and encoded in signed 16-bit integers.
    """

    def __init__(self, source_path):
        self.source_path = source_path
        self.samples = Sampler._load_samples(source_path)

    def get_samples(self, pos, length, amp, fade_in_len, fade_out_len):
        samples = self.samples[pos:pos + length].astype(np.float64)
        samples[:fade_in_len] *= Sampler._fade_in_ramp(fade_in_len, amp)
        samples[-fade_in_len:] *= Sampler._fade_out_ramp(fade_out_len, amp)
        return samples

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
