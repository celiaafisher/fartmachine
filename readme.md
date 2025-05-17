# Fart Machine

This repository contains a simple Python script that generates a random fart sound each time you press Enter. The sound is synthesized on the fly and is different every run.

### How it works

The script now uses a more physically inspired approach. Bandpass-filtered noise around 100–300 Hz forms the base flutter, amplitude is shaped by a series of random pressure bursts and a fast, irregular LFO, and a short comb filter adds cheek-like resonance. Each fart fades out with a natural decay.

## Requirements

- Python 3
- One of the following audio playback commands available on your system: `ffplay`, `aplay`, `afplay`, `play`, `open`, or `xdg-open`.

If none of these commands are available, the script saves the generated sound as a `.wav` file in the current folder and prints its location so you can play it manually.

## Usage

Run the `fart_machine.py` script:

```bash
python3 fart_machine.py
```

Press Enter whenever prompted to hear a newly synthesized fart sound. Use `Ctrl+C` to exit.
