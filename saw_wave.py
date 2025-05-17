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
    """Play a sawtooth wave using sounddevice.

    The frequency is randomly selected between 30 Hz and 45 Hz for each run.
    The duration is clamped to the range [0.1, 3] seconds.

    Returns
    -------
    float
        The randomly selected frequency.
    """
    freq = random.uniform(30.0, 45.0)
    duration = max(0.1, min(3.0, duration))
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    sd.play(wave, sample_rate)
    sd.wait()
    return freq


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Play a low-frequency sawtooth wave")
    parser.add_argument(
        "duration",
        nargs="?",
        type=float,
        default=2.0,
        help="Length of the playback in seconds (clamped to 0.1-3)",
    )
    args = parser.parse_args()
    freq = play_saw_wave(duration=args.duration)
    print(f"Played sawtooth wave at {freq:.2f} Hz")
