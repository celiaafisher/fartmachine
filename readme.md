# Fart Machine

This repository contains a simple Python script that generates a random fart sound each time you press Enter. The sound is synthesized on the fly and is different every run.

### How it works

The script builds a tone whose volume is modulated by a slow oscillator so the sound pulses slightly. A filtered layer of noise adds a windy texture and the whole sound is shaped with an exponential decay so each fart fades out naturally.

## Requirements

- Python 3
- One of the following audio playback commands available on your system: `ffplay`, `aplay`, `afplay`, `play`, `open`, or `xdg-open`.

Each fart is also written to a `.wav` file in the same directory as `fart_machine.py`. If playback fails, you can play the saved file manually.

## Usage

Run the `fart_machine.py` script:

```bash
python3 fart_machine.py
```

Press Enter whenever prompted to hear a newly synthesized fart sound. Use `Ctrl+C` to exit.
