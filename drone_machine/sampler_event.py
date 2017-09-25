import collections


SamplerEvent = collections.namedtuple(
    'SamplerEvent',
    [
        'event_pos',
        'sample_pos',
        'length',
        'amp',
        'fade_in_len',
        'fade_out_len',
    ]
)

