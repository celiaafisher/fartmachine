# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script plays a sawtooth wave using `numpy` and `sounddevice`.
Each run randomly selects a base frequency between **8 Hz** and **20 Hz**, then
applies a low-pass filter whose cutoff frequency is randomly chosen between
**300 Hz** and **3000 Hz**.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Running the script plays a short, randomized sawtooth tone:

```bash
python saw_wave.py
```

The program prints the randomly selected base frequency and low-pass cutoff
each time it runs.
