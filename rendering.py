import ctypes
import multiprocessing
import time
import random
import gc

import numpy

from tqdm import tqdm

import config
import terminal


def samples_needed(voices):
    return int(max(v.keyframes[-1][0] for v in voices))


def normalize(array, value):
    max_value = max(array.max(), abs(array.min()))
    factor = value / max_value
    array *= factor


def split_voices(voices, n_groups):
    """Randomly breaak `voices` into a number of groups.

    Warning: This modifies the contents of `voices`
    """
    random.shuffle(voices)
    return numpy.array_split(voices, n_groups)


class RenderWork:
    def __init__(self, process, progress, progress_bar):
        self.process = process
        self.progress = progress
        self.progress_bar = progress_bar


def render(voices):
    num_samples = samples_needed(voices)
    data_array = multiprocessing.Array(ctypes.c_double, num_samples)
    voice_groups = split_voices(voices, config.processes)

    remaining_work = []
    for group in voice_groups:
        progress = multiprocessing.Value(ctypes.c_ulonglong, 0)
        process = multiprocessing.Process(
            target=render_worker,
            args=(group, data_array, 0, num_samples, progress))
        process.start()
        progress_bar = tqdm(total=num_samples,
                            desc=f'rendering pid {process.pid}')
        remaining_work.append(RenderWork(process, progress, progress_bar))

    render_start_time = time.time()

    # `voices` and `voice_groups` are potentially large, and we don't need
    # them anymore, so let the GC know we're done with them.
    del voices
    del voice_groups
    gc.collect()

    while True:
        for work in remaining_work:
            work.progress_bar.update(work.progress.value - work.progress_bar.n)
            if not work.process.is_alive():
                work.progress_bar.close()
        remaining_work = [w for w in remaining_work if w.process.is_alive()]
        if not remaining_work:
            break
        time.sleep(0.5)

    terminal.clear()

    time_elapsed = round(time.time() - render_start_time, 1)
    print(f'sample rendering completed in {time_elapsed} seconds...')
    samples = numpy.frombuffer(data_array.get_obj())

    print('normalizing data...')
    normalize(samples, 32767)

    print(f'converting to output dtype {config.dtype.__name__}')
    return samples.astype(config.dtype)


def write_samples(chunks, data_array, offset):
    samples = numpy.concatenate(chunks)
    samples.resize((len(data_array),))
    with data_array.get_lock():
        np_array = numpy.frombuffer(data_array.get_obj())[offset:]
        if len(samples) > len(np_array):
            samples.resize(len(np_array))
        np_array += samples


def render_worker(voices, data_array, start, end, progress):
    """Worker process method. Mutates data_array in place with locking."""
    chunks = []
    max_chunks = ((config.worker_data_size * random.uniform(0.8, 1.2))
                  / config.chunk_size)
    last_write_pos = 0
    for pos in range(start, end + config.chunk_size, config.chunk_size):
        chunk = numpy.zeros(config.chunk_size)
        for voice in voices:
            voice_samples = voice.get_samples_at(pos, config.chunk_size)
            if voice_samples is not None:
                chunk += voice_samples
        chunks.append(chunk)
        # No lock needed since we're the only process writing to this
        progress.value = pos

        # Try to keep memory under control by periodically dumping progress
        # to shared memory and invoking the gc.
        if len(chunks) > max_chunks:
            write_samples(chunks, data_array, last_write_pos)
            last_write_pos = pos
            chunks = []
            gc.collect()

    write_samples(chunks, data_array, last_write_pos)


def render_with_single_process(voices):
    """Single-process version of `render`

    Used for profiling purposes.
    """
    num_samples = samples_needed(voices)
    data_array = multiprocessing.Array(ctypes.c_double, num_samples)
    voice_groups = split_voices(voices, config.processes)

    for group in tqdm(voice_groups):
        progress = multiprocessing.Value(ctypes.c_ulonglong, 0)
        render_worker(group, data_array, 0, num_samples, progress)

    render_start_time = time.time()

    time_elapsed = round(time.time() - render_start_time, 1)
    print(f'sample rendering completed in {time_elapsed} seconds...')
    samples = numpy.frombuffer(data_array.get_obj())

    print('normalizing data...')
    normalize(samples, 32767)

    print(f'converting to output dtype {config.dtype.__name__}')
    return samples.astype(config.dtype)
