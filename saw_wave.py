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


def play_saw_wave(duration=2.0, sample_rate=44100):
    """Play a sawtooth wave at a random frequency between 30 and 45 Hz."""
    freq = random.uniform(30, 45)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    sd.play(wave, sample_rate)
    sd.wait()
    return freq


if __name__ == "__main__":
    freq_played = play_saw_wave()
    print(f"Played sawtooth wave at {freq_played:.2f} Hz")
