import math
import os
import random
import shutil
import struct
import subprocess
import time
import wave

SAMPLE_RATE = 44100

class BiquadBandpass:
    def __init__(self, freq, q):
        w0 = 2 * math.pi * freq / SAMPLE_RATE
        alpha = math.sin(w0) / (2 * q)
        b0 = alpha
        b1 = 0.0
        b2 = -alpha
        a0 = 1 + alpha
        a1 = -2 * math.cos(w0)
        a2 = 1 - alpha
        self.b0 = b0 / a0
        self.b1 = b1 / a0
        self.b2 = b2 / a0
        self.a1 = a1 / a0
        self.a2 = a2 / a0
        self.x1 = self.x2 = 0.0
        self.y1 = self.y2 = 0.0

    def process(self, x):
        y = self.b0 * x + self.b1 * self.x1 + self.b2 * self.x2 - self.a1 * self.y1 - self.a2 * self.y2
        self.x2 = self.x1
        self.x1 = x
        self.y2 = self.y1
        self.y1 = y
        return y

def generate_fart(character=0.5):
    """Generate a fart sound as a list of 16-bit samples."""
    character = max(0.0, min(1.0, character))

    attack = 0.01 + random.uniform(0.0, 0.03)
    decay = 0.1 + 0.5 * character
    release = 0.02 + 0.08 * character
    duration = attack + decay + release
    n_samples = int(SAMPLE_RATE * duration)

    pulse_freq = 120 - 90 * character
    pulse_phase = random.uniform(0, 2 * math.pi)
    flutter_freq = random.uniform(5, 15)
    flutter_phase = random.uniform(0, 2 * math.pi)

    low_center = 80 + 200 * (1 - character)
    high_center = 2500
    high_mix = 0.3 + 0.2 * (1 - 2 * character)
    low_mix = 1.0 - high_mix

    brown_gain = 1 + 2.16 * character

    filt_low = BiquadBandpass(low_center, 5.0)
    filt_high = BiquadBandpass(high_center, 5.0)

    pink = 0.0
    brown = 0.0
    samples = []

    for i in range(n_samples):
        t = i / SAMPLE_RATE
        white = random.uniform(-1.0, 1.0)
        pink = 0.97 * pink + 0.03 * white
        brown = 0.98 * brown + 0.02 * white
        noise = pink * (1 - character) + brown_gain * brown * character

        if t < attack:
            env = t / attack
        elif t < attack + decay:
            env = 1 - (t - attack) / decay
        else:
            env = max(0.0, (duration - t) / release)

        pulse = max(0.0, math.sin(2 * math.pi * pulse_freq * t + pulse_phase))
        flutter = 1.0 + 0.3 * math.sin(2 * math.pi * flutter_freq * t + flutter_phase)

        sample = noise * env * pulse * flutter
        low = filt_low.process(sample)
        high = filt_high.process(sample)
        value = low_mix * low + high_mix * high

        fade_samples = int(0.002 * SAMPLE_RATE)
        if n_samples - i <= fade_samples:
            value *= (n_samples - i) / fade_samples

        samples.append(int(max(-1.0, min(1.0, value)) * 32767))

    return samples

def write_wav(samples, path):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack('<' + 'h' * len(samples), *samples))


def play_samples(samples):
    filename = f"fart_{int(time.time() * 1000)}.wav"
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
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
