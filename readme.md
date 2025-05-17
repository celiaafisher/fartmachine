# Fart Machine

This repository demonstrates generating a short sawtooth burst in Python. Each execution produces a slightly different sound by randomizing several parameters.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Running the script will pick a random frequency between 8 and 12 Hz and a random duration between 0.1 and 3 seconds. The waveform is shaped with a quick-attack, quick-release envelope, filtered with a resonant low‑pass and high‑pass stage, run through a mild waveshaper and then thickened by a simple chorus effect. A random “mod wheel” value modulates the high-pass cutoff, drive and chorus mix each run.

```bash
python saw_wave.py
```

The selected frequency, duration, attack and release times are printed before playback. Sound playback may not work in all environments.
