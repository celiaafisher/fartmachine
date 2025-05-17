# Fart Machine

This repository contains a simple Python script that generates a random fart sound each time you press Enter. The sound is synthesized on the fly and is different every run.

### How it works

The script builds a tone whose volume is modulated by a slow oscillator so the sound pulses slightly. A filtered layer of noise adds a windy texture and the whole sound is shaped with an exponential decay so each fart fades out naturally.

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

---

### Web version

A JavaScript class `FartSynthesizer` implements the same fart generator using the Web Audio API. Load `fart_machine_web.js` in a browser and call one of the preset methods, for example:

```html
<script src="fart_machine_web.js"></script>
<script>
  const synth = new FartSynthesizer();
  synth.longFart();
</script>
```

This version exposes parameters like duration, wetness and bubbliness for experimentation.
