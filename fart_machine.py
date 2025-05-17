import math
import os
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import wave

SAMPLE_RATE = 44100

def _wave_sample(wave_type: str, phase: float) -> float:
    """Return a waveform sample for the given phase."""
    r = phase % (2 * math.pi)
    if wave_type == 'sine':
        return math.sin(r)
    if wave_type == 'saw':
        return 2 * (r / (2 * math.pi)) - 1
    if wave_type == 'square':
        return 1.0 if math.sin(r) >= 0 else -1.0
    if wave_type == 'pulse':
        return 1.0 if (r % (2*math.pi)) < math.pi * 0.3 else -1.0
    if wave_type == 'triangle':
        return 2 * abs(2 * (r / (2 * math.pi)) - 1) - 1
    return 0.0


def _adsr_envelope(t: float, duration: float, attack: float, decay: float,
                   sustain: float, release: float) -> float:
    """Simple ADSR envelope."""
    if t < attack:
        return t / max(attack, 1e-6)
    if t < attack + decay:
        return 1 - (1 - sustain) * ((t - attack) / max(decay, 1e-6))
    if t < duration - release:
        return sustain
    if t < duration:
        return sustain * (1 - (t - (duration - release)) / max(release, 1e-6))
    return 0.0


def generate_fart(duration=1.0):
    """Generate a more flexible fart sound and return sample values."""
    # Oscillator setup
    osc1_wave = random.choice(['saw', 'pulse', 'sine'])
    osc2_wave = random.choice(['square', 'sine'])
    base_freq = random.uniform(70, 110)
    detune = random.uniform(-1.5, 1.5)

    # Pitch envelope parameters
    pitch_env_amt = random.uniform(-0.3, 0.3)
    pitch_env_time = 0.15

    # Amplitude envelope parameters
    attack = 0.02
    decay = 0.3
    sustain = 0.2
    release = 0.2

    n_samples = int(SAMPLE_RATE * duration)
    samples = []

    # LFO for amplitude pulsing
    lfo_rate = random.uniform(8, 16)
    lfo_phase = random.uniform(0, 2 * math.pi)

    phase1 = 0.0
    phase2 = 0.0
    noise_lp = 0.0

    for i in range(n_samples):
        t = i / SAMPLE_RATE

        # Pitch envelope (simple exponential decay)
        if t < pitch_env_time:
            pitch_mod = pitch_env_amt * (1 - t / pitch_env_time)
        else:
            pitch_mod = 0.0

        freq1 = base_freq * (1 + pitch_mod)
        freq2 = base_freq * (1 + detune * 0.01)

        phase1 += 2 * math.pi * freq1 / SAMPLE_RATE
        phase2 += 2 * math.pi * freq2 / SAMPLE_RATE

        tone = 0.5 * (_wave_sample(osc1_wave, phase1) + _wave_sample(osc2_wave, phase2))

        # Noise with low-pass filter for windy texture
        raw_noise = random.uniform(-1, 1)
        noise_lp += 0.05 * (raw_noise - noise_lp)

        # LFO amplitude modulation
        lfo_val = math.sin(2 * math.pi * lfo_rate * t + lfo_phase)

        env = _adsr_envelope(t, duration, attack, decay, sustain, release)

        value = (tone + 0.4 * noise_lp) * env * (1 + 0.2 * lfo_val)

        # 2 ms fade out to avoid pops
        if i > n_samples - int(0.002 * SAMPLE_RATE):
            fade = (n_samples - i) / (0.002 * SAMPLE_RATE)
            value *= fade

        samples.append(int(max(-1.0, min(1.0, value)) * 32767))

    return samples

def write_wav(samples, path):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack('<' + 'h'*len(samples), *samples))


def play_samples(samples):
    base = os.path.dirname(os.path.abspath(__file__))
    filename = time.strftime('fart_%Y%m%d_%H%M%S.wav')
    path = os.path.join(base, filename)
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
