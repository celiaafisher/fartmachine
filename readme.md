# Fart Machine

This repository contains a simple example of generating and playing a sawtooth wave in Python.

The `saw_wave.py` script generates a randomly tuned sawtooth wave, shapes it with a random amplitude envelope, applies a low-pass filter, and plays it using `sounddevice`.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run:

```bash
python saw_wave.py
```

Each execution selects a random frequency between 30 and 45 Hz and a random duration between 0.1 and 3 seconds. The amplitude envelope also uses a random attack (5–200 ms) and release (50–700 ms) before playback.
