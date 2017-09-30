from drone_machine import config
from drone_machine.sampler import Sampler


length_weights = [(w[0] * config.sample_rate, w[1]) for w in [
    # (seconds, weight)
    (0.01, 1),
    (0.05, 5),
    (0.1, 1),
    (0.5, 3),
    (1, 5),
    (10, 0)
]]

amp_factor_weights = [
    (0.1, 50),
    (0.5, 3),
    (1, 1),
    (3, 0)
]

samplers = [
    Sampler(
        source='cage_feldman.wav',
        step=config.sample_rate // 10,
        event_prob_factor=5,
        length_weights=length_weights,
        amp_factor_weights=amp_factor_weights
    ),
]
