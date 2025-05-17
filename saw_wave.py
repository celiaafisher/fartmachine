import numpy as np
import sounddevice as sd
import random


def saw_wave(freq, time_array):
    """Generate a sawtooth wave for the given times."""
    return 2.0 * (freq * time_array % 1.0) - 1.0


def apply_envelope(signal, sample_rate, attack=None, release=None):
    """Apply a simple attack/release envelope.

    Parameters
    ----------
    signal : numpy.ndarray
        Input audio signal.
    sample_rate : int
        Samples per second.
    attack : float, optional
        Attack time in seconds. Randomized if ``None``.
    release : float, optional
        Release time in seconds. Randomized if ``None``.

    Returns
    -------
    numpy.ndarray
        Signal multiplied by the envelope.
    float
        Attack time used in seconds.
    float
        Release time used in seconds.
    """
    if attack is None:
        attack = random.uniform(0.005, 0.2)
    if release is None:
        release = random.uniform(0.05, 0.7)

    attack_samples = min(int(attack * sample_rate), len(signal))
    remaining = len(signal) - attack_samples
    release_samples = min(int(release * sample_rate), remaining)

    envelope = np.ones_like(signal)
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    if release_samples > 0:
        envelope[-release_samples:] = np.linspace(1, 0, release_samples)

    return signal * envelope, attack, release


def play_random_saw_wave(sample_rate=44100):
    """Play a sawtooth wave with random settings."""
    freq = random.uniform(30.0, 45.0)
    duration = random.uniform(0.1, 3.0)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    wave, attack, release = apply_envelope(wave, sample_rate)
    print(
        f"Playing {freq:.2f} Hz for {duration:.2f}s "
        f"(attack {attack:.3f}s, release {release:.3f}s)"
    )
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_random_saw_wave()
