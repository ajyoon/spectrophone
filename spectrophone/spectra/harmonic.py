import itertools


def series(fundamental, num_partials):
    return [
        fundamental * o for o in range(1, num_partials + 1)
    ]


def fractal(fundamentals, depth, num_partials):
    if not isinstance(fundamentals, list):
        fundamentals = [fundamentals]
    if depth <= 1:
        return list(itertools.chain.from_iterable([
            series(f, num_partials)
            for f in fundamentals
        ]))

    return list(itertools.chain.from_iterable([
        fractal(list(itertools.chain.from_iterable([series(f, num_partials)])),
                depth - 1,
                num_partials)
        for f in fundamentals
    ]))
