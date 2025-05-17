import numpy as np
import sounddevice as sd


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


def amp_envelope(sample_rate, attack, sustain, release):
    """Create an amplitude envelope."""
    a_len = int(attack * sample_rate)
    s_len = int(sustain * sample_rate)
    r_len = int(release * sample_rate)

    a = np.linspace(0.0, 1.0, a_len, endpoint=False)
    s = np.ones(s_len)
    r = np.linspace(1.0, 0.0, r_len, endpoint=False)

    return np.concatenate([a, s, r])


def play_saw_wave(sample_rate=44100):
    """Play a randomly generated sawtooth wave."""
    freq = np.random.uniform(30, 45)
    duration = np.random.uniform(0.1, 3.0)

    # Pick random attack and release values that fit into the duration
    while True:
        attack = np.random.uniform(0.005, 0.2)
        release = np.random.uniform(0.05, 0.7)
        if attack + release <= duration:
            break

    sustain = duration - attack - release

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = saw_wave(freq, t)
    env = amp_envelope(sample_rate, attack, sustain, release)
    wave = wave[: len(env)] * env

    sd.play(wave, sample_rate)
    sd.wait()

    print(
        f"Played {freq:.2f} Hz for {duration:.2f} s "
        f"(attack {attack:.3f}s, release {release:.3f}s)"
    )


if __name__ == "__main__":
    play_saw_wave()
