import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter


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


def apply_envelope(wave: np.ndarray, sample_rate: int,
                   attack: float, release: float) -> np.ndarray:
    """Apply an amplitude envelope with a squared fade-out."""
    length = wave.size
    env = np.ones(length)

    a_len = int(sample_rate * attack)
    r_len = int(sample_rate * release)

    if a_len > 0:
        env[:a_len] = np.linspace(0, 1, a_len)

    if r_len > 0:
        env[-r_len:] = np.linspace(1, 0, r_len) ** 2

    return wave * env


def lowpass_filter(signal, cutoff_hz, sample_rate, order=2):
    """Apply a simple Butterworth low-pass filter."""
    nyquist = sample_rate / 2.0
    norm_cutoff = cutoff_hz / nyquist
    b, a = butter(order, norm_cutoff, btype="low", analog=False)
    return lfilter(b, a, signal)


def play_saw_wave(duration: float = 2.0, sample_rate: int = 44100) -> None:
    """Play a sawtooth wave with random frequency and filter cutoff."""
    base_freq = np.random.uniform(8, 20)
    cutoff_hz = np.random.uniform(300, 3000)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(base_freq, t)
    wave = lowpass_filter(wave, cutoff_hz, sample_rate)
    wave = apply_envelope(wave, sample_rate, attack=0.05, release=0.1)

    print(
        f"Playing {base_freq:.1f} Hz sawtooth filtered at {cutoff_hz:.0f} Hz"
    )
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()
