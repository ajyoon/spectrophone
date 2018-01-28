class SamplerVoice:

    def __init__(self, sampler):
        self.sampler = sampler
        self.events = []  # list of `SamplerEvent`s

    @property
    def max_sample_pos(self):
        return max((e.event_pos + e.length for e in self.events), default=0)
