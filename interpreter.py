import multiprocessing
import ctypes
import gc
import time
import itertools

from tqdm import tqdm
from blur import rand
import numpy

import config
from voice import Voice
from oscillator import Oscillator
from score import Score
from frequencies import frequencies


scale_pitches = {
    'gf': frequencies[6],
    'bf': frequencies[10],
    'c': frequencies[0] * 2,
    'df': frequencies[1] * 2,
    'ef': frequencies[3] * 2,
    'f': frequencies[5] * 2
}

main_pitch_weights = [
    (scale_pitches['gf'], 10),
    (scale_pitches['bf'], 7),
    (scale_pitches['df'], 10),
    (scale_pitches['f'], 3),
]

scale_pitch_weights = [
    (scale_pitches['gf'], 5),
    (scale_pitches['bf'], 5),
    (scale_pitches['c'], 7),
    (scale_pitches['df'], 3),
    (scale_pitches['ef'], 1),
    (scale_pitches['f'], 3),
]

detune_weights = [
    (0, 100),
    (2, 10),
    (20, 1),
    (50, 0),
]

octave_weights = [
    (1/8, 5),
    (1/4, 15),
    (1/2, 35),
    (1, 7),
    (2, 1),
    (4, 0.5),
    (8, 0.1),
]



def interpret():
    voices = []
    for i in tqdm(range(config.num_voices), 'generating oscillators'):
        base_freq = rand.weighted_choice(scale_pitch_weights)
        detuned_freq = base_freq + rand.pos_or_neg(
            rand.weighted_rand(detune_weights))
        freq = detuned_freq * rand.weighted_choice(octave_weights)
        voices.append(Voice(Oscillator(freq)))

    voices.sort(key=lambda v: v.oscillator.frequency)

    print('interpreting score...')
    score = Score(config.score_path)

    n_groups = config.processes
    remaining_work = []
    for voice_group, amp_map_slice in zip(numpy.array_split(
                                              voices, n_groups),
                                          numpy.array_split(
                                              score.amplitude_map, n_groups)):
        progress = multiprocessing.Value(ctypes.c_ulonglong, 0)
        result_queue = multiprocessing.Queue(maxsize=1)
        process = multiprocessing.Process(
            target=interpret_worker,
            args=(amp_map_slice, voice_group, progress, result_queue)
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


def interpret_worker(amplitude_map, voices, progress, result_queue):
    width = len(amplitude_map[0])
    height = len(amplitude_map)

    # Cache event decisions - use period length that unevenly divides score
    # width so different voices are not aligned
    prob = max(height / len(voices) * 0.5, 0.0001)
    event_prob = prob_bool_cycle(prob, width // 7)

    sample_positions = [(x / width) * config.length * config.sample_rate
                        for x in range(width)]
    y_voice_map = [abs(int((v / len(voices)) * height) - height + 1)
                   for v in range(len(voices))]

    for v in range(len(voices)):
        voice = voices[v]
        for x in range(width):
            if next(event_prob):
                voice.keyframes.append((sample_positions[x],
                                        amplitude_map[y_voice_map[v]][x]))
        voice.finalize(False)
        progress.value = v

    result_queue.put([v for v in voices if len(v.keyframes)])


def prob_bool_cycle(prob, length):
    unrolled = [rand.prob_bool(prob) for i in range(length)]
    return itertools.cycle(unrolled)
