# Fart Machine

This repository contains a simple Python script that generates a random fart sound each time you press Enter. The sound is synthesized on the fly and is different every run.

### How it works

Each fart is synthesized in real time using a single "macro" knob that sweeps
from squeaky to deep. The patch mixes pink and brown noise, shaped by an ADSR
envelope and short pressure pulses. Two parallel band-pass filters add cheek and
edge resonances while a wandering LFO introduces subtle flutter. The finished
sound fades out cleanly so there are no clicks.

## Requirements

- Python 3
- One of the following audio playback commands available on your system: `ffplay`, `aplay`, `afplay`, `play`, `open`, or `xdg-open`.

If none of these commands are available, the script writes the sound to a `.wav`
file in the current directory and prints the path so you can play it manually.

## Usage

Run the `fart_machine.py` script:

```bash
python3 fart_machine.py
```

Press Enter whenever prompted to hear a newly synthesized fart sound. Use `Ctrl+C` to exit.
