# Fart Machine

This repository demonstrates generating a short sawtooth burst in Python. Each execution produces a slightly different sound by randomizing several parameters.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Running the script will pick a random frequency between 30 and 45 Hz and a random duration between 0.1 and 3 seconds. The waveform is shaped with a quick-attack, quick-release envelope and passed through a low-pass filter whose cutoff frequency rises and then falls to create a squelchy effect.

```bash
python saw_wave.py
```

The selected frequency, duration, attack and release times are printed before playback. Sound playback may not work in all environments.
