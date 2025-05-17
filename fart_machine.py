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
    """Generate a unique fart sound and return bytes for a WAV file."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []
    base_freq = random.uniform(60, 120)
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        freq = base_freq - (base_freq * 0.5 * t / duration)
        value = math.sin(2 * math.pi * freq * t)
        value += 0.2 * random.uniform(-1, 1)
        value *= math.exp(-3 * t)
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
