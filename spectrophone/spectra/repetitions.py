import itertools


def octaves(pitch_group, num_octaves):
    """Repeat a pitch group over a given number of octaves.

    Returns a combined list of the given pitch group multiplied
    by successive power-of-twos above the lowest pitch in the
    given group.

    Args:
        pitch_group (list[float]):
        num_octaves (int): Must be greater than 0

    Returns: iter[float]

    Warning: No sorting is performed in this; if the given `pitch_group`
    is not in ascending order or exceeds the size of an octave, the returned
    iterable will not be ascending order either.
    """
    return itertools.chain.from_iterable([
        [p * (2 ** octave) for p in pitch_group]
        for octave in range(num_octaves)
    ])
