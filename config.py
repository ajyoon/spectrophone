import multiprocessing

import numpy


nchannels = 1
sampwidth = 2
framerate = 44100
nframes = 0
comptype = 'NONE'
compname = 'NONE'

wave_params = (
    nchannels,
    sampwidth,
    framerate,
    nframes,
    comptype,
    compname
)

dtype = numpy.int16

chunk_size = 4096

worker_data_size = 128_000_000 // 8  # 128Mb worth of 8-byte doubles
processes = multiprocessing.cpu_count()

silence_threshold = 0.0001

length = 60 * 2  # Seconds

score_path = 'resources/line.png'
