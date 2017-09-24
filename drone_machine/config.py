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

chunk_size = 1024

worker_data_size = 128_000_000 // 8  # 128Mb worth of 8-byte doubles
processes = multiprocessing.cpu_count()

silence_threshold = 2 / 255

length = 60  # Seconds

num_voices = 50

score_path = os.path.join(os.path.dirname(__file__),
                          '..', 'resources', 'test.png')
