import math
import os
import random
import shutil
import struct
import subprocess
import uuid
import wave

SAMPLE_RATE = 44100

def generate_fart(duration=1.5):
    """Generate a unique fart sound and return samples for a WAV file."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []

    base_freq = random.uniform(40, 90)
    wobble_freq = random.uniform(3, 8)
    noise_amt = random.uniform(0.3, 0.6)
    sine_amt = random.uniform(0.2, 0.5)

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        envelope = math.exp(-2 * t) * (1 + 0.5 * math.sin(2 * math.pi * wobble_freq * t))
        noise = noise_amt * random.uniform(-1, 1)
        tone = sine_amt * math.sin(2 * math.pi * base_freq * t)
        value = (noise + tone) * envelope
        samples.append(int(max(-1.0, min(1.0, value)) * 32767))

    return samples

def write_wav(samples, path):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack('<' + 'h'*len(samples), *samples))


def play_samples(samples):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"fart_{uuid.uuid4().hex}.wav"
    path = os.path.join(script_dir, filename)
    write_wav(samples, path)

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
