import numpy as np

from spectrophone import config


def _period_length(frequency):
    return round(config.sample_rate / frequency)


class Waveform:

    @staticmethod
    def generate_period(frequency):
        raise NotImplementedError()


class Sine(Waveform):

    @staticmethod
    def generate_period(frequency):
        period_length = _period_length(frequency)
        return (np.sin(
            np.arange(period_length)
            * (frequency * ((np.pi * 2) / config.sample_rate)))
        ) * 32767


class Square(Waveform):

    @staticmethod
    def generate_period(frequency):
        period_length = _period_length(frequency)
        return np.concatenate(
            (np.full(period_length // 2, 32767),
             np.full(period_length // 2, -32767))
        )


class Triangle(Waveform):

    @staticmethod
    def generate_period(frequency):
        period_length = _period_length(frequency)
        return np.concatenate(
            (np.linspace(-32767, 32767, num=period_length // 2),
             np.linspace(32767, -32767, num=period_length // 2))
        )
