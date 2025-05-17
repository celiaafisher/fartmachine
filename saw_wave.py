import numpy as np
import sounddevice as sd
import random


def saw_wave(freq, time_array):
    """Generate a sawtooth wave.

    Parameters
    ----------
    freq : float
        Frequency of the wave in Hz.
    time_array : numpy.ndarray
        Array of time values.

    Returns
    -------
    numpy.ndarray
        The sawtooth waveform sampled at the times provided.
    """
    return 2.0 * (freq * time_array % 1.0) - 1.0


def play_saw_wave(freq=None, duration=2.0, sample_rate=44100):
    """Play a sawtooth wave using sounddevice.

    Parameters
    ----------
    freq : float or None
        If ``None``, a random frequency between 30 Hz and 45 Hz will be used.
    duration : float
        Length of the sound in seconds. Values outside the range 0.1–3 will
        be clamped.
    sample_rate : int
        Audio sample rate in Hz.
    """
    if freq is None:
        freq = random.uniform(30.0, 45.0)

    duration = max(0.1, min(duration, 3.0))

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()
