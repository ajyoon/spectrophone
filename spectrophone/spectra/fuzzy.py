from blur import rand


def generate(num, pitch_weights, detune_weights,
             octave_weights):
    frequencies = []
    for i in range(num):
        base_freq = rand.weighted_choice(pitch_weights)
        detuned_freq = base_freq + rand.pos_or_neg(
            rand.weighted_rand(detune_weights))
        freq = round(detuned_freq * rand.weighted_choice(octave_weights), 1)
        frequencies.append(freq)
    return sorted(frequencies)
