import struct
import wave

import numpy as np
from tqdm import tqdm

from spectrophone import config


def write(out_path, ch0_samples, ch1_samples=None):
    with wave.open(out_path, 'wb') as out:
        print(f'writing audio data to {out_path}')
        out.setsampwidth(config.sampwidth)
        out.setframerate(config.sample_rate)

        if ch1_samples is None:
            out.setnchannels(1)
            out.writeframes(ch0_samples)
        else:
            out.setnchannels(2)
            out.writeframes(
                np.ravel((ch0_samples, ch1_samples), order='F')
            )
