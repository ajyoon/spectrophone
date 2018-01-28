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

worker_data_size = 800_000_000 // 8  # ~n Mb worth of 8-byte doubles
processes = multiprocessing.cpu_count()

silence_threshold = 0

osc_step = int(sample_rate / 1)

resources_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 '..', 'resources'))
