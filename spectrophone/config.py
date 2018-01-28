import multiprocessing
import os

import numpy


sampwidth = 2
sample_rate = 44100
nframes = 0
comptype = 'NONE'
compname = 'NONE'

dtype = numpy.int16

chunk_size = 1024

worker_data_size = 800_000_000 // 8  # ~n Mb worth of 8-byte doubles
processes = multiprocessing.cpu_count()

silence_threshold = 0

default_osc_step = int(sample_rate / 1)

max_freq = sample_rate - 1000

resources_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 '..', 'resources'))
