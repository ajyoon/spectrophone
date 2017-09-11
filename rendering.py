import numpy

import config


def samples_needed(voices):
    max_sample = 0
    for voice in voices:
        for keyframe in voice.keyframes:
            if max_sample < keyframe.sample_pos:
                max_sample = keyframe.sample_pos
    return max_sample


def render(voices):
    chunks = []
    for pos in range(0, samples_needed(voices), config.chunk_size):
        chunk = numpy.zeros(config.chunk_size, config.dtype)
        for voice in voices:
            chunk = chunk + voice.get_samples_at(pos, config.chunk_size)
        chunks.append(chunk)
    return numpy.concatenate(chunks)
