import math
import os
import random
import shutil
import struct
import subprocess
import sys
import time
import wave

SAMPLE_RATE = 44100

def generate_fart(duration=1.5):
    """Generate a unique fart sound and return sample values."""
    n_samples = int(SAMPLE_RATE * duration)
    samples = []

    # Build a sequence of pressure bursts with random timing and intensity
    bursts = []
    n_bursts = random.randint(3, 6)
    for _ in range(n_bursts):
        length = random.uniform(0.1, 0.4)
        start = random.uniform(0, max(0.0, duration - length))
        amplitude = random.uniform(0.6, 1.0)
        bursts.append((start, length, amplitude))
    bursts.sort(key=lambda b: b[0])

    # Simple bandpass filter variables for 100-300 Hz
    dt = 1.0 / SAMPLE_RATE
    rc_lp = 1.0 / (2 * math.pi * 300)
    rc_hp = 1.0 / (2 * math.pi * 100)
    alpha_lp = dt / (rc_lp + dt)
    alpha_hp = rc_hp / (rc_hp + dt)
    lp = 0.0
    hp = 0.0
    prev_lp = 0.0

    # Resonant comb filter to simulate cheek resonance
    comb_delay = int(0.01 * SAMPLE_RATE)
    comb = [0.0] * comb_delay
    comb_i = 0

    flutter_freq = random.uniform(15, 35)
    flutter_phase = random.uniform(0, 2 * math.pi)

    def envelope(t):
        amp = 0.0
        for start, length, a in bursts:
            if start <= t < start + length:
                u = t - start
                attack = 0.1 * length
                if u < attack:
                    amp += a * (u / attack)
                else:
                    decay_t = (u - attack) / max(0.001, length - attack)
                    amp += a * (1.0 - decay_t)
        return min(amp, 1.0)

    for i in range(n_samples):
        t = i / SAMPLE_RATE

        # Bandpass filtered noise for the base fluttering sound
        noise = random.uniform(-1, 1)
        lp += alpha_lp * (noise - lp)
        bp = hp + alpha_hp * (lp - prev_lp)
        prev_lp = lp
        hp = bp

        # Irregular LFO for vibration
        flutter_freq += random.uniform(-0.1, 0.1)
        flutter_freq = max(15, min(35, flutter_freq))
        lfo = math.sin(2 * math.pi * flutter_freq * t + flutter_phase)

        amp = envelope(t) * (0.8 + 0.2 * lfo)

        value = bp * amp

        # Comb filter resonance
        res = comb[comb_i]
        comb[comb_i] = value + res * 0.5
        value += res * 0.3
        comb_i = (comb_i + 1) % comb_delay

        # Overall natural decay
        value *= math.exp(-2.0 * t)

        samples.append(int(max(-1.0, min(1.0, value)) * 32767))

    return samples

def write_wav(samples, path):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack('<' + 'h'*len(samples), *samples))


def play_samples(samples):
    # Save the WAV file in the current working directory instead of a temp
    # location so it can be easily accessed after playback.
    timestamp = int(time.time() * 1000)
    path = os.path.join(os.getcwd(), f"fart_{timestamp}.wav")
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
