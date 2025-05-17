# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script plays a randomly generated sawtooth wave using `numpy` and `sounddevice`.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Running the script will generate a new wave each time. The frequency is chosen
between **30 Hz** and **45 Hz**, while the duration varies from **0.1–3 s**. The
volume envelope also changes on every run with an attack of **5–200 ms** and a
release of **50–700 ms**.

To play a wave run:

```bash
python saw_wave.py
```
