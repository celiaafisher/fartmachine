# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script plays a low-pitched sawtooth wave using `numpy` and `sounddevice`.
Each time it runs, the frequency is randomly chosen between **30&nbsp;Hz** and **45&nbsp;Hz**.
The playback duration is clamped to be between **0.1** and **3** seconds.
After playback, the chosen frequency is printed to the console.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with an optional duration argument (defaults to 2&nbsp;seconds):

```bash
python saw_wave.py
```
