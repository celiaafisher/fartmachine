import math
import os
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import wave

SAMPLE_RATE = 44100

def generate_fart(duration=1.5):
    """Generate a unique fart sound and return sample values."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []

    base_freq = random.uniform(60, 120)
    lfo_freq = random.uniform(0.5, 2.0)
    lfo_phase = random.uniform(0, 2 * math.pi)

    noise_lp = 0.0
    noise_lp_amp = 0.0

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # Sweep frequency downward slightly during the sound
        freq = base_freq - (base_freq * 0.5 * t / duration)

        tone = math.sin(2 * math.pi * freq * t)

        # Low frequency oscillator with a bit of random variation for pulsing
        noise_lp_amp = 0.98 * noise_lp_amp + 0.02 * random.uniform(-1, 1)
        amp_lfo = 0.8 + 0.2 * math.sin(2 * math.pi * lfo_freq * t + lfo_phase)
        amplitude = amp_lfo + 0.2 * noise_lp_amp

        # Heavier noise filtered with a simple low-pass filter for windy texture
        raw_noise = random.uniform(-1, 1)
        noise_lp = 0.93 * noise_lp + 0.07 * raw_noise

        value = (tone + 0.4 * noise_lp) * amplitude

        # Natural exponential decay over time
        value *= math.exp(-2.5 * t)

        samples.append(int(max(-1.0, min(1.0, value)) * 32767))

    return samples

def write_wav(samples, path):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack('<' + 'h'*len(samples), *samples))


def play_samples(samples):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        write_wav(samples, tmp.name)
        path = tmp.name

    players = [
        ['ffplay', '-nodisp', '-autoexit', path],
        ['aplay', path],
        ['afplay', path],
        ['play', path],
        ['open', path],
        ['xdg-open', path],
    ]
    for cmd in players:
        if shutil.which(cmd[0]):
            try:
                subprocess.run(cmd, check=True)
                os.unlink(path)
                return True
            except Exception:
                pass
    print(f"Saved sound to {path}, but no audio player was found.")
    return False


def main():
    print("Press Enter to hear a fart (Ctrl+C to quit)...")
    while True:
        try:
            input()
        except EOFError:
            break
        samples = generate_fart()
        play_samples(samples)


if __name__ == '__main__':
    main()
