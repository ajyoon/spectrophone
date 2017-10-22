from spectrophone.sampler import Sampler


class SamplerVoice:

    def __init__(self, sampler):
        self.sampler = sampler
        self.events = []  # list of `SamplerEvent`s
