import collections


SamplerEvent = collections.namedtuple(
    'SamplerEvent',
    [
        'event_pos',   # When this event occurs, in samples
        'sample_pos',  # Where in the complete sample this
                       # event starts, in samples
        'length',
        'amp',
        'fade_in_len',
        'fade_out_len',
    ]
)
