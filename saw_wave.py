import numpy as np
import sounddevice as sd


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


def play_saw_wave(freq=10, duration=2.0, sample_rate=44100):
    """Play a sawtooth wave using sounddevice."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()
