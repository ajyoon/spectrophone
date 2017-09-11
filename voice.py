import numpy


class Voice:

    def __init__(self, oscillator):
        self.oscillator = oscillator
        self.keyframes = []

    def last_frame_at(self, sample_pos):
        return max((k for k in self.keyframes if k.sample_pos <= sample_pos),
                   key=lambda k: k.sample_pos,
                   default=None)

    def next_frame_at(self, sample_pos):
        return min((k for k in self.keyframes if k.sample_pos > sample_pos),
                   key=lambda k: k.sample_pos,
                   default=None)

    def get_samples_at(self, sample_pos, chunk_size):
        last_frame = self.last_frame_at(sample_pos)
        next_frame = self.next_frame_at(sample_pos)
        if last_frame is None:
            return 0
        if next_frame is None:
            amplitude = last_frame.amplitude
        else:
            amplitude = numpy.interp(
                sample_pos,
                [last_frame.sample_pos, next_frame.sample_pos],
                [last_frame.amplitude, next_frame.amplitude])
        return self.oscillator.get_samples(chunk_size, amplitude)
