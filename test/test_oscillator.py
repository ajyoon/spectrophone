import numpy as np


from drone_machine.oscillator import Oscillator


def test_get_samples_is_smooth():
    actual_osc = Oscillator(440)
    actual_samples = np.concatenate([actual_osc.get_samples(440, 1),
                                     actual_osc.get_samples(440, 1)])
    expected_samples = Oscillator(440).get_samples(880, 1)
    np.testing.assert_almost_equal(actual_samples, expected_samples)
