# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script plays a low-pitched sawtooth wave using `numpy` and `sounddevice`.
Each execution chooses random parameters so the sound varies every run:
- frequency between 30 Hz and 45 Hz
- duration between 0.1 s and 2.0 s
- attack between 0.2 s and 0.5 s
- release between 0.3 s and 0.9 s

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the script to play a randomized sawtooth wave:

```bash
python saw_wave.py
```

The program prints the selected frequency, duration, attack, and release settings before playback.
