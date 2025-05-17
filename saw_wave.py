import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter


def saw_wave(freq: float, time_array: np.ndarray) -> np.ndarray:
    """Generate a sawtooth wave."""
    return 2.0 * (freq * time_array % 1.0) - 1.0


def amplitude_envelope(length: int, sample_rate: int, attack: float, release: float) -> np.ndarray:
    """Create an amplitude envelope with linear attack and release."""
    env = np.ones(length)
    a_len = int(sample_rate * attack)
    r_len = int(sample_rate * release)
    if a_len > 0:
        env[:a_len] = np.linspace(0, 1, a_len)
    if r_len > 0:
        env[-r_len:] = np.linspace(1, 0, r_len)
    return env


def lowpass_filter(signal: np.ndarray, cutoff_hz: float, sample_rate: int, order: int = 2) -> np.ndarray:
    """Apply a basic resonant low-pass filter."""
    nyquist = sample_rate / 2.0
    norm_cutoff = cutoff_hz / nyquist
    b, a = butter(order, norm_cutoff, btype="low", analog=False)
    return lfilter(b, a, signal)


def play_saw_wave(sample_rate: int = 44100) -> None:
    """Generate a random sawtooth burst and play it."""
    freq = np.random.uniform(30.0, 45.0)
    duration = np.random.uniform(0.1, 3.0)
    attack = np.random.uniform(0.005, 0.2)
    release = np.random.uniform(0.05, 0.7)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    env = amplitude_envelope(len(wave), sample_rate, attack, release)
    wave *= env
    wave = lowpass_filter(wave, cutoff_hz=1500, sample_rate=sample_rate)

    print(
        f"Playing {freq:.1f} Hz for {duration:.2f} s "
        f"(attack={attack:.3f}s, release={release:.3f}s)"
    )
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()
