import wave

import numpy as np
from tqdm import tqdm

from drone_machine import config


def write(out_path, samples):
    with wave.open(out_path, 'wb') as out:
        print(f'writing audio data to {out_path}')
        out.setparams(config.wave_params)
        write_chunks = np.array_split(
            samples,
            len(samples) // (config.sample_rate * 30))
        for write_chunk in tqdm(write_chunks, f'writing to {out_path}'):
            out.writeframes(write_chunk)
