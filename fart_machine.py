import math
import os
import struct
import wave
import sys

SAMPLE_RATE = 44100


def saw_wave(freq, duration, sample_rate=SAMPLE_RATE):
    n_samples = int(duration * sample_rate)
    data = []
    for n in range(n_samples):
        t = n / sample_rate
        value = 2 * ((t * freq) - math.floor(0.5 + t * freq))
        data.append(value)
    return data


def square_wave(freq, duration, sample_rate=SAMPLE_RATE):
    n_samples = int(duration * sample_rate)
    data = []
    for n in range(n_samples):
        t = n / sample_rate
        value = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
        data.append(value)
    return data


def envelope(attack, decay, sustain_level, duration, fs=SAMPLE_RATE):
    attack_samples = int(attack * fs)
    decay_samples = int(decay * fs)
    sustain_samples = max(0, int(duration * fs) - attack_samples - decay_samples)
    env = []
    for i in range(attack_samples):
        env.append(i / attack_samples if attack_samples else 1.0)
    for i in range(decay_samples):
        env.append(1 - (1 - sustain_level) * (i / decay_samples))
    for _ in range(sustain_samples):
        env.append(sustain_level)
    return env


def diff_signal(signal):
    if not signal:
        return []
    diff = [signal[0]]
    for i in range(1, len(signal)):
        diff.append(signal[i] - signal[i - 1])
    return diff


def dynamic_lowpass(signal, cutoff_env, fs=SAMPLE_RATE):
    dt = 1.0 / fs
    y = 0.0
    out = []
    for x, c in zip(signal, cutoff_env):
        rc = 1.0 / (2 * math.pi * c)
        alpha = dt / (rc + dt)
        y += alpha * (x - y)
        out.append(y)
    return out


def highpass(signal, cutoff, fs=SAMPLE_RATE):
    if not signal:
        return []
    dt = 1.0 / fs
    rc = 1.0 / (2 * math.pi * cutoff)
    alpha = rc / (rc + dt)
    out = []
    y = 0.0
    prev_x = signal[0]
    for x in signal:
        y = alpha * (y + x - prev_x)
        out.append(y)
        prev_x = x
    return out


def saturate(signal, drive):
    return [math.tanh(x * drive) for x in signal]


def generate_fart(duration=5.0, sample_rate=SAMPLE_RATE):
    lfo_freq = 3.0
    raw_saw = saw_wave(lfo_freq, duration, sample_rate)
    square = square_wave(lfo_freq, duration, sample_rate)
    impulses = diff_signal(raw_saw)

    env = envelope(0.4, 2.0, 0.0, duration, sample_rate)
    cutoff_env = [500 + e * 2000 for e in env]
    filtered = dynamic_lowpass(impulses, cutoff_env, sample_rate)

    wavetable_env = envelope(0.0, 1.0, 0.0, duration, sample_rate)
    combined = []
    for s, sq, w in zip(filtered, square, wavetable_env):
        combined.append((1 - w) * s + w * sq)

    cleaned = highpass(combined, 200, sample_rate)
    saturated = saturate(cleaned, 3.0)

    samples = [int(max(-1.0, min(1.0, x)) * 32767) for x in saturated]
    return samples


def write_wav(samples, path, sample_rate=SAMPLE_RATE):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack('<' + 'h' * len(samples), *samples))


def main():
    output = sys.argv[1] if len(sys.argv) > 1 else 'fart.wav'
    samples = generate_fart()
    write_wav(samples, output)
    print(f'Wrote {output}')


if __name__ == '__main__':
    main()
