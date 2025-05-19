import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter
from typing import Union

# Global state for MS-20 filter emulation
ic1eq = 0.0
ic2eq = 0.0

# Precomputed wavetable bank ranging from a pure sawtooth to a square-like
# waveform. Each table contains one cycle with 512 samples.
WAVETABLE_SIZE = 64
_TABLE_LEN = 512

_phase = np.linspace(0.0, 1.0, _TABLE_LEN, endpoint=False)
_base_saw = 2.0 * _phase - 1.0
_base_square = np.sign(_base_saw)
wavetables = np.stack([
    (1.0 - w) * _base_saw + w * _base_square
    for w in np.linspace(0.0, 1.0, WAVETABLE_SIZE)
])


def saw_wave(freq: float, time_array: np.ndarray) -> np.ndarray:
    """Generate a sawtooth wave."""
    return 2.0 * (freq * time_array % 1.0) - 1.0


def amplitude_envelope(
    length: int,
    sample_rate: int,
    attack: float,
    decay: float,
    sustain_level: float,
    release: float,
) -> np.ndarray:
    """Create a basic ADSR amplitude envelope.

    Parameters
    ----------
    length : int
        Total envelope length in samples.
    sample_rate : int
        Sample rate in Hz.
    attack : float
        Attack time in seconds.
    decay : float
        Decay time in seconds.
    sustain_level : float
        Sustain level as a fraction of 1.0.
    release : float
        Release time in seconds.
    """

    a_len = int(sample_rate * attack)
    d_len = int(sample_rate * decay)
    r_len = int(sample_rate * release)
    s_len = max(length - (a_len + d_len + r_len), 0)

    attack_seg = np.linspace(0.0, 1.0, a_len, endpoint=False)
    decay_seg = np.linspace(1.0, sustain_level, d_len, endpoint=False)
    sustain_seg = np.full(s_len, sustain_level)
    release_seg = np.linspace(sustain_level, 0.0, r_len, endpoint=True)

    env = np.concatenate([attack_seg, decay_seg, sustain_seg, release_seg])
    return env[:length]


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

    `cutoff_hz may be a scalar or an array matching signal for
    per-sample modulation. `drive scales the input before the filtering
    step; values above `1.0 introduce non-linearity via a tanh stage.
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


def resonant_highpass(
    signal: np.ndarray,
    cutoff_hz: Union[float, np.ndarray],
    q: float,
    sample_rate: int,
    drive: float = 1.0,
) -> np.ndarray:
    """Two-pole SVF high-pass with resonance and drive."""

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
            out[i] = np.tanh(high)
    else:
        for i, x in enumerate(signal):
            f = 2.0 * np.sin(np.pi * cutoff_hz[i] / sample_rate)
            x_driven = x * drive
            high = x_driven - low - damping * band
            band += f * high
            low += f * band
            out[i] = np.tanh(high)
    return out


def ms20_lowpass(
    signal: np.ndarray,
    cutoff_hz: Union[float, np.ndarray],
    res: Union[float, np.ndarray],
    drive: Union[float, np.ndarray],
    sr: int,
) -> np.ndarray:
    """Simple MS-20 style low-pass filter with drive inside the feedback loop.

    Parameters
    ----------
    signal : np.ndarray
        Input signal buffer.
    cutoff_hz : float or np.ndarray
        Filter cutoff frequency in Hz. Can be a scalar or per-sample array.
    res : float or np.ndarray
        Resonance amount as a scalar or per-sample array.
    drive : float or np.ndarray
        Drive applied inside the feedback loop; higher values add more
        saturation. Can be a scalar or per-sample array.
    sr : int
        Sample rate in Hz.
    """

    global ic1eq, ic2eq
    out = np.zeros_like(signal)
    for i, x in enumerate(signal):
        f = (
            2.0 * np.sin(np.pi * cutoff_hz / sr)
            if np.isscalar(cutoff_hz)
            else 2.0 * np.sin(np.pi * cutoff_hz[i] / sr)
        )
        this_res = res if np.isscalar(res) else res[i]
        this_drive = drive if np.isscalar(drive) else drive[i]

        v1 = (f * (x - ic2eq) + ic1eq) / (1.0 + f * (f + this_res))
        v2 = f * v1 + ic2eq
        x = np.tanh(this_drive * v2)
        ic1eq = 2.0 * v1 - ic1eq
        ic2eq = 2.0 * x - ic2eq
        out[i] = x
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


def limiter(x: np.ndarray, thresh: float = 0.95) -> np.ndarray:
    """Simple limiter using tanh soft clipping."""
    return np.tanh(x / thresh) * thresh


def chorus(
    signal: np.ndarray,
    sample_rate: int,
    depth_s: float = 0.005,
    rate_hz: float = 1.0,
    phase: float = 0.0,
) -> np.ndarray:
    """Mono chorus using an LFO-modulated delay line, wet-only.

    Parameters
    ----------
    signal : np.ndarray
        Input audio buffer.
    sample_rate : int
        Sample rate in Hz.
    depth_s : float, default 0.005
        Maximum delay depth in seconds.
    rate_hz : float, default 1.0
        LFO rate in Hertz.
    phase : float, default 0.0
        Starting phase of the LFO as a fraction of one cycle.
    """
    n = len(signal)
    phase_rad = 2 * np.pi * phase
    lfo = np.sin(np.pi * rate_hz * np.arange(n) / sample_rate + phase_rad)
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
        out[i] = delayed
    return out


def ensemble_chorus(signal: np.ndarray, sample_rate: int) -> np.ndarray:
    """Three-voice chorus for a thicker ensemble sound."""
    c1 = chorus(signal, sample_rate, rate_hz=0.9, depth_s=0.005, phase=0.0)
    c2 = chorus(signal, sample_rate, rate_hz=1.1, depth_s=0.006, phase=0.33)
    c3 = chorus(signal, sample_rate, rate_hz=1.0, depth_s=0.004, phase=0.66)
    dry = signal
    wet = (c1 + c2 + c3) / 3
    return 0.5 * dry + 0.5 * wet


def apply_modwheel(signal: np.ndarray, sample_rate: int, mod: float) -> np.ndarray:
    """Deprecated: kept for backwards compatibility."""
    hp_cut = 100 + mod * 900

    sig = resonant_highpass(signal, cutoff_hz=hp_cut, q=0.8, sample_rate=sample_rate)
    sig = chorus(sig, sample_rate, depth_s=0.005, rate_hz=0.8)
    return sig


def play_saw_wave(sample_rate: int = 44100) -> None:
    """Generate a random sawtooth burst and play it."""
    raw_freq = np.random.uniform(20.0, 35.0)
    duration = np.random.uniform(0.5, 3.0)
    attack = np.random.uniform(0.005, 0.2)
    decay = np.random.uniform(0.05, 0.3)
    sustain_level = np.random.uniform(0.4, 0.8)
    release = np.random.uniform(0.05, 0.2)
    mod = np.random.uniform(0.0, 1.0)

    freq = raw_freq

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # ----- Amp envelope (env1)
    amp_env = amplitude_envelope(
        len(t),
        sample_rate,
        attack,
        decay,
        sustain_level,
        release,
    )

    # ----- Wavetable envelope (env3)
    wt_env = filter_envelope(
        length=len(t),
        sample_rate=sample_rate,
        attack=0.0,
        decay=1.0,
    )

    phase = (freq * t) % 1.0
    table_pos = wt_env * (WAVETABLE_SIZE - 1)
    wave = np.zeros_like(phase)
    square = np.zeros_like(phase)
    for i in range(len(phase)):
        idx = table_pos[i]
        lo = int(np.floor(idx))
        hi = min(lo + 1, WAVETABLE_SIZE - 1)
        frac = idx - lo
        p = int(phase[i] * _TABLE_LEN)
        samp_lo = wavetables[lo][p]
        samp_hi = wavetables[hi][p]
        wave[i] = (1.0 - frac) * samp_lo + frac * samp_hi
        square[i] = wavetables[-1][p]

    wave *= amp_env
    square *= amp_env

    # Additional square modulation via mod wheel
    wave = (1 - mod * 0.2) * wave + (mod * 0.2) * square

    # ----- Pre-drive before filtering
    wave = saturator(wave, drive=1.5)

    # ----- Filter envelope (env2)
    filt_env = filter_envelope(
        length=len(wave),
        sample_rate=sample_rate,
        attack=0.4,
        decay=2.0,
    )

    # Exponential mapping for a more musical cutoff sweep
    min_cf, max_cf = 100.0, 1500.0
    cutoff_env = min_cf * (max_cf / min_cf) ** filt_env
    cutoff = cutoff_env * (1 + 0.5 * mod)

    # ----- MS-20 style low-pass with internal drive
    q = 0.95
    ic1eq = ic2eq = 0.0  # reset filter state
    wave = ms20_lowpass(
        wave,
        cutoff_hz=cutoff,
        res=1.0 / q,
        drive=6.0,
        sr=sample_rate,
    )

    # ----- Remove rumble with slight resonance
    wave = resonant_highpass(
        signal=wave,
        cutoff_hz=200.0,
        q=1.2,
        sample_rate=sample_rate,
        drive=1.2,
    )

    # ----- Extra drive after filtering
    wave = saturator(wave, drive=2.0)

    # ----- 3-voice ensemble chorus
    wave = ensemble_chorus(wave, sample_rate)

    wave = limiter(wave)

    print(
        f"Playing {freq:.1f} Hz for {duration:.2f} s "
        f"(attack={attack:.3f}s, decay={decay:.3f}s, "
        f"sustain={sustain_level:.2f}, release={release:.3f}s, mod={mod:.2f})"
    )
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()