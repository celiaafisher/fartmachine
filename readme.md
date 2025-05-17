# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script plays a low-pitched sawtooth wave using `numpy`, `sounddevice`, and a basic low-pass filter from `scipy`.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Running the script generates a short, filtered saw wave each time using
random values close to the defaults:

- **Base frequency** – around 10 Hz (randomly between 8 Hz and 12 Hz)
- **Low-pass cutoff** – around 1500 Hz (randomly between 1000 Hz and 2000 Hz)

To hear it, run:

```bash
python saw_wave.py
```
