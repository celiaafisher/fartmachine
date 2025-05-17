# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script plays a low-pitched sawtooth wave using `numpy` and `sounddevice`.
Each execution randomly selects a frequency between **30 Hz** and **45 Hz** and a duration
between **0.1 s** and **3 s**. A short attack and a more intense fade-out are also
randomized for every run.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the script to play a randomly generated wave:

```bash
python saw_wave.py
```
