import multiprocessing
import os

import numpy


nchannels = 1
sampwidth = 2
sample_rate = 44100
nframes = 0
comptype = 'NONE'
compname = 'NONE'

wave_params = (
    nchannels,
    sampwidth,
    sample_rate,
    nframes,
    comptype,
    compname
)

dtype = numpy.int16

chunk_size = 2048

worker_data_size = 128_000_000 // 8  # 128Mb worth of 8-byte doubles
processes = multiprocessing.cpu_count()

silence_threshold = 2 / 255

length = 60 * 10  # Seconds

num_osc_voices = 0
num_sampler_voices = 1

sampler_step = int(0.1 * sample_rate)

sampler_event_prob_factor = 0.03

score_path = os.path.join(os.path.dirname(__file__),
                          '..', 'resources', 'long.png')

samples_dir = os.path.join(os.path.dirname(__file__), '..', 'resources')
samples_paths = {
    filename: os.path.join(samples_dir, filename)
    for filename in [
        'cage_feldman.wav'
    ]}
