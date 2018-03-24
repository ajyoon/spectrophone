import matplotlib.pyplot as plt


def plot_voices(voices):
    """Plot and display the keyframes of a list of voices.

    Assumes that `Voice.finalize()` has been called on all voices.
    """

    plt.figure(1)

    for i, voice in enumerate(voices):
        frames = voice.keyframes
        plt.plot(
            [f[0] for f in frames],
            [f[1] + voice.oscillator.frequency for f in frames]
        )

    plt.show()
