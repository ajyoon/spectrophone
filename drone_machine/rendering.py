import ctypes
import multiprocessing
import time
import random
import gc

import numpy

from tqdm import tqdm

from drone_machine import config
from drone_machine import terminal


def normalize(array, value):
    max_value = max(array.max(), abs(array.min()))
    factor = value / max_value if max_value > 0 else 1
    array *= factor


def split_voices(voices, n_groups):
    """Randomly breaak `voices` into a number of groups.

    Warning: This modifies the contents of `voices`
    """
    random.shuffle(voices)
    return [group for group in numpy.array_split(voices, n_groups)
            if len(group)]


class RenderWork:
    def __init__(self, process, progress, progress_bar):
        self.process = process
        self.progress = progress
        self.progress_bar = progress_bar


def render(osc_voices, sampler_voices):
    render_start_time = time.time()

    data_array = multiprocessing.Array(ctypes.c_double, config.total_samples)

    if sampler_voices:
        render_samplers(sampler_voices, data_array)

    # Render oscillators
    osc_voice_groups = split_voices(osc_voices, config.processes)

    remaining_work = []
    for group in osc_voice_groups:
        progress = multiprocessing.Value(ctypes.c_ulonglong, 0)
        process = multiprocessing.Process(
            target=render_osc_worker,
            args=(group, data_array, 0, config.total_samples, progress))
        process.start()
        progress_bar = tqdm(total=config.total_samples,
                            desc='rendering pid ' + str(process.pid))
        remaining_work.append(RenderWork(process, progress, progress_bar))

    # `osc_voices` and `osc_voice_groups` are potentially large, and we don't
    # need them anymore, so let the GC know we're done with them.
    del osc_voices
    del osc_voice_groups
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


def render_osc_worker(osc_voices, data_array, start, end, progress):
    """Worker process method. Mutates data_array in place with locking."""
    chunks = []
    max_chunks = ((config.worker_data_size * random.uniform(0.8, 1.2))
                  / config.chunk_size)
    last_write_pos = 0
    for pos in range(start, end + config.chunk_size, config.chunk_size):
        chunk = numpy.zeros(config.chunk_size)
        for voice in osc_voices:
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


def render_samplers(sampler_voices, data_array):
    with data_array.get_lock():
        out_array = numpy.frombuffer(data_array.get_obj())
        for voice in tqdm(sampler_voices, 'rendering samplers'):
            for event in voice.events:
                start = event.event_pos
                stop = start + event.length
                out_array[start:stop] += voice.sampler.get_samples(
                    event.sample_pos,
                    event.length,
                    event.amp,
                    event.fade_in_len,
                    event.fade_out_len)
