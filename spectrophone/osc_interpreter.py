import multiprocessing
import ctypes
import gc
import time
import itertools

from tqdm import tqdm
from blur import rand
import numpy as np

from spectrophone import config
from spectrophone.voice import Voice


def interpret(score, oscillators, length_sec,
              step=config.default_osc_step):
    """Interpret a score into keyframes in a series of given oscillators

    Args:
        score (Score):
        oscillators ([Oscillator]):
        length_sec (float): The length, in seconds, of the desired output.
        step: The frequency, in samples, of keyframe opportunities for the
            generated voices.

    Returns: [Voice]
    """
    voices = [Voice(o) for o in oscillators]

    n_groups = config.processes
    remaining_work = []
    for voice_group, amp_map_slice in zip(np.array_split(
                                              voices, n_groups)[::-1],
                                          np.array_split(
                                              score.amplitude_map, n_groups)):
        if not len(voice_group):
            continue
        progress = multiprocessing.Value(ctypes.c_ulonglong, 0)
        result_queue = multiprocessing.Queue(maxsize=1)
        process = multiprocessing.Process(
            target=interpret_worker,
            args=(amp_map_slice, voice_group,
                  length_sec, step, progress, result_queue)
        )
        process.start()
        remaining_work.append(
            InterpretWork(process, result_queue, progress, len(voice_group)))

    del voices
    del score
    gc.collect()

    interpreted_voices = []

    while True:
        for work in remaining_work:
            work.progress_bar.update(work.progress.value - work.progress_bar.n)
            if not work.result_queue.empty():
                interpreted_voices.extend(work.result_queue.get())
                work.progress_bar.close()
        remaining_work = [w for w in remaining_work if w.process.is_alive()]
        if not remaining_work:
            break
        time.sleep(0.5)

    return interpreted_voices


class InterpretWork:
    def __init__(self, process, result_queue, progress, total):
        self.process = process
        self.progress = progress
        self.progress_bar = tqdm(total=total,
                                 desc=f'interpreting pid {process.pid}')
        self.result_queue = result_queue


def prob_bool_cycle(prob, length):
    return itertools.cycle([rand.prob_bool(prob) for i in range(length)])


def interpret_worker(
        amplitude_map, voices, length_sec, step, progress, result_queue):

    total_samples = int(length_sec * config.sample_rate)

    width = len(amplitude_map[0])
    height = len(amplitude_map)

    # Cache event decisions - use period length that unevenly divides score
    # width so different voices are not aligned
    prob = max((height / len(voices)) / 10, 0.00001)
    event_positions = range(0, total_samples, step)
    num_events = total_samples // step
    event_prob = prob_bool_cycle(prob, int(num_events * (19 / 7)))

    y_voice_map = [abs(int((v / len(voices)) * height) - height + 1)
                   for v in range(len(voices))]

    for v in range(len(voices)):
        voice = voices[v]
        for event_pos in event_positions:
            if next(event_prob):
                x = int((event_pos / total_samples) * width)
                voice.keyframes.append((event_pos,
                                        amplitude_map[y_voice_map[v]][x]))
        voice.finalize(False)
        progress.value = v

    result_queue.put([v for v in voices if len(v.keyframes)])
