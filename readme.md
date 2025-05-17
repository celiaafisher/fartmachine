# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script plays a sawtooth wave using `numpy` and `sounddevice`.
Each time you run it, the frequency is randomly selected between 30 Hz and 45 Hz
and the duration is randomly selected between 0.1 s and 3 s.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Simply run the script to play a randomly generated sawtooth wave:

```bash
python saw_wave.py
```
