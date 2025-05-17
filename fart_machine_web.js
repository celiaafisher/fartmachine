class FartSynthesizer {
  constructor(context) {
    this.context = context || new (window.AudioContext || window.webkitAudioContext)();
  }

  // Generate hybrid white/brown noise based on wetness (0.0 - 1.0)
  _createNoiseBuffer(duration, wetness) {
    const length = Math.floor(duration * this.context.sampleRate);
    const buffer = this.context.createBuffer(1, length, this.context.sampleRate);
    const data = buffer.getChannelData(0);
    let brown = 0;
    for (let i = 0; i < length; i++) {
      const white = Math.random() * 2 - 1;
      brown = (brown + 0.02 * white) / 1.02;
      data[i] = (1 - wetness) * brown + wetness * white;
    }
    return buffer;
  }

  // Schedule an envelope with bubble dips and frequency modulation
  _applyEnvelope(gainNode, filterNode, options, startTime) {
    const intensity = options.intensity;
    const attack = options.suddenness;
    const duration = options.duration;
    const bubbles = Math.max(1, Math.floor(options.bubbliness));
    const bubbleWidth = 0.05;
    const baseFreq = options.frequency;
    const bubbleSpacing = (duration - attack) / bubbles;

    gainNode.gain.setValueAtTime(0.0, startTime);
    gainNode.gain.linearRampToValueAtTime(intensity, startTime + attack);
    filterNode.frequency.setValueAtTime(baseFreq, startTime);

    let t = startTime + attack;
    for (let i = 0; i < bubbles; i++) {
      const jitter = (Math.random() * 0.6 + 0.7) * bubbleSpacing;
      const dip = intensity * (0.5 + Math.random() * 0.2);
      gainNode.gain.linearRampToValueAtTime(dip, t);
      filterNode.frequency.linearRampToValueAtTime(baseFreq * (0.8 + Math.random() * 0.4), t);
      gainNode.gain.linearRampToValueAtTime(intensity, t + bubbleWidth);
      filterNode.frequency.linearRampToValueAtTime(baseFreq, t + bubbleWidth);
      t += jitter;
    }
    gainNode.gain.linearRampToValueAtTime(0.0, startTime + duration);
  }

  // Play a single fart according to the provided parameters
  playFart(params = {}) {
    const opts = Object.assign({
      duration: 1.0,
      wetness: 0.5,
      intensity: 0.8,
      frequency: 220,
      bubbliness: 4,
      suddenness: 0.1,
    }, params);

    const buffer = this._createNoiseBuffer(opts.duration, opts.wetness);
    const source = this.context.createBufferSource();
    source.buffer = buffer;

    const band = this.context.createBiquadFilter();
    band.type = 'bandpass';
    band.frequency.value = opts.frequency;
    band.Q.value = 2.8;

    const peak = this.context.createBiquadFilter();
    peak.type = 'peaking';
    peak.frequency.value = opts.frequency * 1.5;
    peak.Q.value = 2.8;
    peak.gain.value = 6;

    const gain = this.context.createGain();
    gain.gain.value = 0;

    source.connect(band);
    band.connect(peak);
    peak.connect(gain);
    gain.connect(this.context.destination);

    const now = this.context.currentTime;
    this._applyEnvelope(gain, band, opts, now);

    source.start(now);
    source.stop(now + opts.duration + 0.1);

    const cleanup = () => {
      source.disconnect();
      band.disconnect();
      peak.disconnect();
      gain.disconnect();
    };
    source.onended = cleanup;
    setTimeout(cleanup, (opts.duration + 0.5) * 1000);
  }

  // Preset helpers
  quickFart() {
    this.playFart({ duration: Math.random() * 0.4 + 0.3, wetness: Math.random() * 0.3 + 0.1, suddenness: 0.05, bubbliness: Math.floor(Math.random() * 3) + 1 });
  }

  longFart() {
    this.playFart({ duration: Math.random() * 1.5 + 1.5, wetness: Math.random() * 0.4 + 0.3, suddenness: 0.1, bubbliness: Math.floor(Math.random() * 8) + 8 });
  }

  wetFart() {
    this.playFart({ duration: Math.random() * 0.8 + 0.7, wetness: Math.random() * 0.3 + 0.7, suddenness: 0.08, bubbliness: Math.floor(Math.random() * 4) + 4 });
  }

  squeakyFart() {
    this.playFart({ duration: Math.random() * 0.7 + 0.5, wetness: 0.1, frequency: Math.random() * 350 + 350, bubbliness: Math.floor(Math.random() * 3) + 3 });
  }
}

// Example usage:
// const fart = new FartSynthesizer();
// fart.quickFart();
