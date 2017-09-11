import config


class Keyframe:

    def __init__(self, time, amplitude):
        """
        Args:
            time (float): Time in seconds of this frame
            amplitude (float): 0-1 amplitude at this frame.
        """
        self.time = time
        self.amplitude = amplitude

    @property
    def sample_pos(self):
        """int: The actual sample this occurs in."""
        return int(config.framerate * self.time)
