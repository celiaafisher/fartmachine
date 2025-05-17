import numpy as np
import sounddevice as sd


def saw_wave(freq: float, time_array: np.ndarray) -> np.ndarray:
    """Generate a sawtooth wave."""
    return 2.0 * (freq * time_array % 1.0) - 1.0


def apply_envelope(wave: np.ndarray, sample_rate: int,
                   attack: float, release: float) -> np.ndarray:
    """Apply an amplitude envelope with intense fade-out."""
    length = wave.size
    env = np.ones(length)

    a_len = int(sample_rate * attack)
    r_len = int(sample_rate * release)

    if a_len > 0:
        env[:a_len] = np.linspace(0, 1, a_len)

    if r_len > 0:
        # Use squared fade-out for a steeper drop
        env[-r_len:] = np.linspace(1, 0, r_len) ** 2

    return wave * env


def play_saw_wave(sample_rate: int = 44100) -> None:
    """Play a sawtooth wave with random parameters."""
    freq = np.random.uniform(30, 45)
    duration = np.random.uniform(0.1, 3.0)
    attack = np.random.uniform(0.005, 0.2)
    release = np.random.uniform(0.05, 0.7)

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    wave = apply_envelope(wave, sample_rate, attack, release)

    print(f"Playing {freq:.1f} Hz for {duration:.2f} s (attack={attack:.3f}s, release={release:.3f}s)")
    sd.play(wave, sample_rate)
    sd.wait()


if __name__ == "__main__":
    play_saw_wave()
