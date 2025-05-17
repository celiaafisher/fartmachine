# Fart Machine

This repository contains a simple example of generating a sawtooth wave in Python.

The `saw_wave.py` script will play a sawtooth tone using `numpy` and `sounddevice`.  Each
run chooses random parameters so you get slightly different results every time.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Simply run the script:

```bash
python saw_wave.py
```

When run, it picks a random frequency between **30&nbsp;Hz** and **45&nbsp;Hz** and a random
length between **0.1** and **3&nbsp;seconds**.  It also applies a volume envelope with a
random attack time from **5&nbsp;ms** to **200&nbsp;ms** and a random release time from
**50&nbsp;ms** to **700&nbsp;ms**.
