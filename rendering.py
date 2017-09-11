import logging

import numpy
import progressbar

import config


def samples_needed(voices):
    max_sample = 0
    for voice in voices:
        for keyframe in voice.keyframes:
            if max_sample < keyframe.sample_pos:
                max_sample = keyframe.sample_pos
    return max_sample


def normalize(array, value):
    print(array.max())
    print(array.min())
    max_value = max(array.max(), abs(array.min()))
    for i in range(len(array)):
        array[i] = (array[i] / max_value) * value


def render(voices):
    progressbar.streams.wrap_stderr()
    logging.basicConfig()

    bar = progressbar.ProgressBar()

    chunks = []
    for pos in bar(range(0, samples_needed(voices), config.chunk_size)):
        chunk = numpy.zeros(config.chunk_size)
        for voice in voices:
            chunk = chunk + voice.get_samples_at(pos, config.chunk_size)
        chunks.append(chunk)

    samples = numpy.concatenate(chunks)
    normalize(samples, 32767)
    return samples.astype(config.dtype)
