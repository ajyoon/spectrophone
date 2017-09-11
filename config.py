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
