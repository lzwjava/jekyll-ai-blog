---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: 'Analog Modulation Techniques: AM, FM, PM'
translated: false
type: note
---

### Modulation Techniques: AM, FM, and PM

In the context of communication systems and signal processing, **AM**, **FM**, and **PM** refer to fundamental **analog modulation techniques**. These methods are used to encode (or "modulate") an information-carrying signal (like audio or data) onto a higher-frequency carrier wave for efficient transmission over mediums like radio waves, cables, or wireless channels. While they're primarily associated with analog communication, they can intersect with analog-to-digital (A/D) and digital-to-analog (D/A) conversions in hybrid systems—such as when digitally sampled signals are modulated for transmission or when received modulated signals are digitized.

Here's a breakdown of each:

- **AM (Amplitude Modulation)**:
  The amplitude (strength or height) of the carrier wave is varied in proportion to the amplitude of the modulating signal, while the carrier's frequency remains constant. This is simple and widely used in AM radio broadcasting. It's susceptible to noise because interference affects the amplitude directly.
  *Example*: In voice transmission, louder sounds increase the carrier's amplitude peaks.

- **FM (Frequency Modulation)**:
  The frequency of the carrier wave is varied according to the amplitude and frequency of the modulating signal, while the carrier's amplitude stays constant. FM provides better noise resistance and is common in FM radio, TV sound, and two-way radios.
  *Example*: Higher-pitched audio shifts the carrier frequency up or down proportionally.

- **PM (Phase Modulation)**:
  The phase (timing or shift) of the carrier wave is altered based on the modulating signal's changes, with constant amplitude and frequency. PM is similar to FM (they're mathematically related via differentiation) and is often used in digital systems like phase-shift keying (PSK), but in analog form, it's applied in some satellite and mobile communications.
  *Example*: A change in the modulating signal advances or delays the carrier's waveform cycle.

#### Relation to A/D and D/A Conversions
These techniques are more directly tied to analog transmission, but in modern systems:
- During **D/A conversion**, a digital signal might be reconstructed into an analog modulating waveform before applying AM/FM/PM to prepare it for RF (radio frequency) transmission.
- In **A/D conversion**, a received analog modulated signal (e.g., FM radio) is demodulated first, then sampled and quantized into digital form.

For deeper dives, check out resources on analog modulation in signal processing.

[Analog Modulation Techniques](https://en.wikipedia.org/wiki/Modulation#Analog_modulation_methods)
[FM vs AM Comparison](https://www.electronics-tutorials.ws/accircuits/amplitude-modulator.html)
