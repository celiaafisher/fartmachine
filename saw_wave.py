import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter


def cutoff_envelope(
    length: int,
    sample_rate: int,
    attack: float,
    release: float,
    start_hz: float,
    peak_hz: float,
) -> np.ndarray:
    """Create a cutoff envelope that rises then falls."""
    env = np.full(length, peak_hz)
    a_len = int(sample_rate * attack)
    r_len = int(sample_rate * release)
    if a_len > 0:
        env[:a_len] = np.linspace(start_hz, peak_hz, a_len)
    if r_len > 0:
        env[-r_len:] = np.linspace(peak_hz, start_hz, r_len)
    return env


def dynamic_lowpass_filter(
    signal: np.ndarray, cutoff_env: np.ndarray, sample_rate: int
) -> np.ndarray:
    """Apply a simple one-pole low-pass filter with variable cutoff."""
    out = np.zeros_like(signal)
    prev = 0.0
    dt = 1.0 / sample_rate
    for i, (x, cutoff) in enumerate(zip(signal, cutoff_env)):
        rc = 1.0 / (2.0 * np.pi * cutoff)
        alpha = dt / (rc + dt)
        prev = prev + alpha * (x - prev)
        out[i] = prev
    return out


def saw_wave(freq: float, time_array: np.ndarray) -> np.ndarray:
    """Generate a sawtooth wave."""
    return 2.0 * (freq * time_array % 1.0) - 1.0


def amplitude_envelope(length: int, sample_rate: int, attack: float, release: float) -> np.ndarray:
    """Create an amplitude envelope with linear attack and quick release."""
    env = np.ones(length)
    a_len = int(sample_rate * attack)
    r_len = int(sample_rate * release)
    if a_len > 0:
        env[:a_len] = np.linspace(0, 1, a_len)
    if r_len > 0:
        env[-r_len:] = np.linspace(1, 0, r_len)
    return env


def lowpass_filter(
    signal: np.ndarray, cutoff_hz: float, sample_rate: int, order: int = 2
) -> np.ndarray:
    """Apply a basic resonant low-pass filter with fixed cutoff."""
    nyquist = sample_rate / 2.0
    norm_cutoff = cutoff_hz / nyquist
    b, a = butter(order, norm_cutoff, btype="low", analog=False)
    return lfilter(b, a, signal)


def play_saw_wave(sample_rate: int = 44100) -> None:
    """Generate a random sawtooth burst and play it."""
    freq = np.random.uniform(30.0, 45.0)
    duration = np.random.uniform(0.1, 3.0)
    attack = np.random.uniform(0.005, 0.2)
    release = np.random.uniform(0.05, 0.2)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    env = amplitude_envelope(len(wave), sample_rate, attack, release)
    wave *= env

    cutoff_start = np.random.uniform(200.0, 500.0)
    cutoff_peak = np.random.uniform(2000.0, 3000.0)
    cutoff_attack = np.random.uniform(0.01, 0.1)
    cutoff_release = np.random.uniform(0.1, 0.3)
    cutoff_env = cutoff_envelope(
        len(wave),
        sample_rate,
        attack=cutoff_attack,
        release=cutoff_release,
        start_hz=cutoff_start,
        peak_hz=cutoff_peak,
    )
    wave = dynamic_lowpass_filter(wave, cutoff_env, sample_rate)

    print(
        f"Playing {freq:.1f} Hz for {duration:.2f} s "
        f"(attack={attack:.3f}s, release={release:.3f}s, "
        f"cutoff={cutoff_start:.0f}-{cutoff_peak:.0f} Hz)"
    )
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()
