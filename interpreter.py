from tqdm import tqdm
from blur import rand

import config
from voice import Voice
from oscillator import Oscillator
from score import Score
from keyframe import Keyframe
from frequencies import frequencies


num_voices = 1000

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


def value_of(color):
    return sum(color) / 3


def interpret():
    print('generating frequencies...')
    voices = []
    for i in range(num_voices):
        base_freq = rand.weighted_choice(scale_pitch_weights)
        detuned_freq = base_freq + rand.pos_or_neg(
            rand.weighted_rand(detune_weights))
        freq = detuned_freq * rand.weighted_choice(octave_weights)
        voices.append(Voice(Oscillator(freq)))
        voices.sort(key=lambda v: v.oscillator.frequency)

    print('interpreting score...')
    score = Score(config.score_path)

    width = len(score.data[0])
    height = len(score.data)

    for x in tqdm(range(width), 'Generating events'):
        time = (x / width) * config.length
        for v_index in range(len(voices)):
            if rand.prob_bool(0.08):
                y = abs(int((v_index / len(voices)) * height)
                        - height + 1)
                amp = abs((value_of(score.data[y][x]) / 255) - 1)
                voices[v_index].keyframes.append(Keyframe(time, amp))

    for voice in voices:
        voice.finalize()

    return voices
