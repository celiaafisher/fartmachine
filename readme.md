# Fart Machine

This repository contains a simple Python script that generates a random fart sound each time you press Enter. The sound is synthesized on the fly and is different every run.

### How it works

The generator now layers multiple oscillators with a short pitch sweep to mimic sudden gas release. A filtered noise source adds wind, while an ADSR envelope and an amplitude LFO shape the dynamics for more natural fluttering. Each fart is written to the script directory so you can replay it later if your system lacks an audio player.

## Requirements

- Python 3
- One of the following audio playback commands available on your system: `ffplay`, `aplay`, `afplay`, `play`, `open`, or `xdg-open`.

If none of these commands are available, the script saves the generated sound as a `.wav` file in the same directory so you can play it manually later.

## Usage

Run the `fart_machine.py` script:

```bash
python3 fart_machine.py
```

Press Enter whenever prompted to hear a newly synthesized fart sound. Use `Ctrl+C` to exit.
