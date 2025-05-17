# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script plays a low-pitched sawtooth wave using `numpy` and `sounddevice`.
Each run picks a new random frequency between 30 Hz and 45 Hz. Durations
are clamped to the range 0.1–3 seconds.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the script to play a randomly pitched sawtooth wave. The default duration is
2&nbsp;seconds (values outside 0.1–3&nbsp;seconds are clamped):

```bash
python saw_wave.py
```
