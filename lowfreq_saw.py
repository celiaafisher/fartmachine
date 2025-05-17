import os
import numpy as np
import wave

try:
    import simpleaudio as sa
    PLAYBACK_AVAILABLE = True
except ImportError:
    sa = None
    PLAYBACK_AVAILABLE = False

SAMPLE_RATE = 44100
FREQ = 3.0
DURATION = 5.0


def saw_wave(freq: float, duration: float, sample_rate: int) -> np.ndarray:
    """Generate a normalized sawtooth wave (-1.0 to 1.0)."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 2 * (t * freq - np.floor(0.5 + t * freq))


if __name__ == "__main__":
    input("Press Enter to generate the LFO sawtooth sound...")
    data = saw_wave(FREQ, DURATION, SAMPLE_RATE)
    audio = np.int16(data * 32767)

    filename = os.path.join(os.path.dirname(__file__), "lfo_saw.wav")
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    print(f"Saved {filename}")

    if PLAYBACK_AVAILABLE:
        sa.WaveObject(audio.tobytes(), 1, 2, SAMPLE_RATE).play().wait_done()
    else:
        print("Install 'simpleaudio' for playback.")
