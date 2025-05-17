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


def lowpass_filter(signal: np.ndarray, cutoff_hz: float, sample_rate: int,
                   order: int = 2) -> np.ndarray:
    """Apply a low-pass Butterworth filter to the signal."""
    nyquist = sample_rate / 2.0
    norm_cutoff = cutoff_hz / nyquist
    b, a = butter(order, norm_cutoff, btype="low", analog=False)
    return lfilter(b, a, signal)


def play_saw_wave(sample_rate: int = 44100, duration: float = 2.0) -> None:
    """Play a filtered sawtooth wave with slight randomization."""
    base_freq = np.random.uniform(8.0, 12.0)
    cutoff_hz = np.random.uniform(1000.0, 2000.0)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(base_freq, t)
    filtered = lowpass_filter(wave, cutoff_hz, sample_rate)

    print(
        f"Playing {base_freq:.2f} Hz saw wave with {cutoff_hz:.0f} Hz low-pass filter"
    )
    sd.play(filtered, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()
