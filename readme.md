# Fart Machine

This repository contains a small script that generates random sawtooth bursts using
`numpy`, `scipy`, and `sounddevice`.

Running the script plays a saw wave with a new random frequency, duration, and
envelope every time.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with:

```bash
python saw_wave.py
```

Each run will choose:

- **Frequency:** 30–45 Hz
- **Duration:** 0.1–3 seconds
- **Attack:** 5–200 ms
- **Release:** 50–700 ms

The waveform is passed through a resonant low‑pass filter around 1500 Hz with a
tiny amount of random variation to keep things fresh.
