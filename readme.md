# Fart Machine

This repository contains a simple Python script that generates a random fart sound each time you press Enter. The sound is synthesized on the fly and is different every run.

## Requirements

- Python 3
- One of the following audio playback commands available on your system: `ffplay`, `aplay`, `afplay`, `play`, `open`, or `xdg-open`.

If none of these commands are available, the script saves the generated sound to a temporary `.wav` file and prints its location so you can play it manually.

## Usage

Run the `fart_machine.py` script:

```bash
python3 fart_machine.py
```

Press Enter whenever prompted to hear a newly synthesized fart sound. Use `Ctrl+C` to exit.
