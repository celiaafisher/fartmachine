# Fart Machine

This repository demonstrates generating a short sawtooth burst in Python. Each
execution produces a slightly different sound by randomizing several parameters.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Running the script will pick a random frequency between 40 and 80 Hz and a random duration between 0.5 and 3 seconds. The sawtooth is morphed toward a crude pulse wave via a second envelope, filtered with a resonant low-pass and high-pass stage, run through additional drive and finally limited. A simple chorus still thickens the sound, while a random “mod wheel” value modulates the high-pass cutoff and chorus depth each run.

```bash
python saw_wave.py
```

The selected frequency, duration, attack and release times are printed before playback. Sound playback may not work in all environments.
