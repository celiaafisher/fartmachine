import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter
from typing import Union


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


def filter_envelope(
    length: int,
    sample_rate: int,
    attack: float,
    decay: float,
) -> np.ndarray:
    """Create a filter envelope with attack-decay and zero sustain."""
    env = np.zeros(length)
    a_len = int(sample_rate * attack)
    d_len = int(sample_rate * decay)

    a_end = min(a_len, length)
    if a_end > 0:
        env[:a_end] = np.linspace(0.0, 1.0, a_end, endpoint=False)

    d_end = min(d_len, length - a_end)
    if d_end > 0:
        env[a_end : a_end + d_end] = np.linspace(1.0, 0.0, d_end, endpoint=False)

    return env


def resonant_lowpass(
    signal: np.ndarray,
    cutoff_hz: Union[float, np.ndarray],
    q: float,
    sample_rate: int,
    drive: float = 1.0,
) -> np.ndarray:
    """Two-pole SVF with resonance and analogue-style drive.

    ``cutoff_hz`` may be a scalar or an array matching ``signal`` for
    per-sample modulation. ``drive`` scales the input before the filtering
    step; values above ``1.0`` introduce non-linearity via a ``tanh`` stage.
    """

    damping = 1.0 / max(q, 1e-6)
    low = 0.0
    band = 0.0
    out = np.zeros_like(signal)

    if np.isscalar(cutoff_hz):
        f = 2.0 * np.sin(np.pi * cutoff_hz / sample_rate)
        for i, x in enumerate(signal):
            x_driven = x * drive
            high = x_driven - low - damping * band
            band += f * high
            low += f * band
            low = np.tanh(low)
            out[i] = low
    else:
        for i, x in enumerate(signal):
            f = 2.0 * np.sin(np.pi * cutoff_hz[i] / sample_rate)
            x_driven = x * drive
            high = x_driven - low - damping * band
            band += f * high
            low += f * band
            low = np.tanh(low)
            out[i] = low
    return out


def highpass_filter(
    signal: np.ndarray,
    cutoff_hz: float,
    sample_rate: int,
    order: int = 2,
) -> np.ndarray:
    """Basic Butterworth high-pass filter."""
    nyquist = sample_rate / 2.0
    norm_cutoff = cutoff_hz / nyquist
    b, a = butter(order, norm_cutoff, btype="high", analog=False)
    return lfilter(b, a, signal)


def saturator(signal: np.ndarray, drive: float) -> np.ndarray:
    """Simple waveshaper with controllable drive."""
    return np.tanh(drive * signal)


def chorus(
    signal: np.ndarray,
    sample_rate: int,
    depth_s: float = 0.005,
    rate_hz: float = 1.0,
    mix: float = 0.5,
) -> np.ndarray:
    """Mono chorus using an LFO-modulated delay line."""
    n = len(signal)
    lfo = np.sin(2 * np.pi * rate_hz * np.arange(n) / sample_rate)
    delay_samples = (depth_s * sample_rate) * (0.5 * (lfo + 1))
    out = np.zeros(n)
    for i in range(n):
        d = delay_samples[i]
        idx = i - d
        if idx <= 0:
            delayed = 0.0
        else:
            lo, hi = int(np.floor(idx)), int(np.ceil(idx))
            frac = idx - lo
            delayed = (1 - frac) * signal[lo] + frac * signal[min(hi, n - 1)]
        out[i] = mix * delayed + (1 - mix) * signal[i]
    return out


def apply_modwheel(signal: np.ndarray, sample_rate: int, mod: float) -> np.ndarray:
    """Map mod ∈ [0,1] to filter, drive and chorus parameters."""
    hp_cut = 100 + mod * 900
    drive = 1 + mod * 4
    mix = 0.2 + mod * 0.4

    sig = highpass_filter(signal, hp_cut, sample_rate)
    sig = saturator(sig, drive)
    sig = chorus(sig, sample_rate, depth_s=0.005, rate_hz=0.8, mix=mix)
    return sig


def play_saw_wave(sample_rate: int = 44100) -> None:
    """Generate a random sawtooth burst and play it."""
    freq = np.random.uniform(20.0, 35.0)
    duration = np.random.uniform(0.5, 3.0)
    attack = np.random.uniform(0.005, 0.2)
    release = np.random.uniform(0.05, 0.2)
    mod = np.random.uniform(0.0, 1.0)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    env = amplitude_envelope(len(wave), sample_rate, attack, release)
    wave *= env
    filt_env = filter_envelope(len(wave), sample_rate, attack=0.4, decay=2.0)
    cutoff = 100 + filt_env * 1400  # sweep 100 Hz -> 1500 Hz
    wave = resonant_lowpass(
        wave, cutoff_hz=cutoff, q=0.8, sample_rate=sample_rate, drive=1.8
    )
    wave = apply_modwheel(wave, sample_rate, mod)

    print(
        f"Playing {freq:.1f} Hz for {duration:.2f} s "
        f"(attack={attack:.3f}s, release={release:.3f}s, mod={mod:.2f})"
    )
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()
