import numpy


class Voice:

    def __init__(self, oscillator):
        self.oscillator = oscillator
        self.keyframes = []
        self.last_frame_i = 0
        self._last_keyframe_i = 0

    def finalize(self):
        """Finalize the voice's keyframes.

        Must be called before `get_samples_at` may be safely called.
        """
        if not self.keyframes:
            self.get_samples_at = lambda _: None
        else:
            self.keyframes.sort(key=lambda k: k.sample_pos)

    def get_samples_at(self, sample_pos, chunk_size):
        if self.last_frame_i == len(self.keyframes) - 1:
            return self.oscillator.get_samples(chunk_size,
                                               self.keyframes[-1].amplitude)

        # Safe against index errors assuming `finalize` has been called.
        last_frame = self.keyframes[self.last_frame_i]
        next_frame = self.keyframes[self.last_frame_i + 1]
        amplitude = numpy.interp(
                sample_pos,
                [last_frame.sample_pos, next_frame.sample_pos],
                [last_frame.amplitude, next_frame.amplitude])

        # Prepare for next iteration
        if sample_pos >= self.keyframes[self.last_frame_i + 1].sample_pos:
                self.last_frame_i += 1

        # Render
        return self.oscillator.get_samples(chunk_size, amplitude)
