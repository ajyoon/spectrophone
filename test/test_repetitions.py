from spectrophone.spectra import repetitions


def test_octaves():

    assert list(repetitions.octaves([10, 11, 12], 2)) == [
        10, 11, 12, 20, 22, 24
    ]
