---
audio: false
generated: true
image: false
lang: en
layout: post
title: Audio LED Visualizer
translated: false
type: note
---

Uploaded. The LED will now flash in response to sound picked up by the mic on A0. Open **Tools → Serial Plotter** in the Arduino IDE to see the amplitude waveform in real time.

---

## But you asked for *complicated*…

Here's what's possible when you take this further:

### 1. Frequency-based effects (FFT)

Instead of just "loud = on", split the sound into **bass / mids / treble** and drive different LEDs per band. The **Arduino FHT library** (Fast Hartley Transform) runs a full FFT on 256 samples at ~38 kHz. You could drive an **LED strip** where:

- **Bass** (kick drum) → red LEDs flash
- **Vocals / mids** → green LEDs pulse
- **Hi-hats / treble** → blue LEDs shimmer

### 2. Addressable LED strip (WS2812B / NeoPixel)

A strip of individually controllable RGB LEDs driven by one pin. A 30-60 LED strip costs ~$10. With **FastLED** library you can do:

- Beat detection → color waves cascade down the strip
- Peak frequency → rainbow sweeps
- Volume → brightness or pattern speed

### 3. Beat detection algorithm

Instead of raw amplitude, implement a **real beat detector**:

- Running average of amplitude (automatic threshold)
- Debounce — ignore re-triggers within ~200ms (actual beat can't be faster)
- True BPM tracking → lights sync *rhythmically*, not just randomly

### 4. Wireless: Bluetooth speaker integration

- Arduino + Bluetooth module (HC-05/HC-06)
- Steal the audio signal from your phone via Bluetooth
- The LED strip reacts to what's playing on your phone, no wires

### 5. Full build example

```
[Phone / PC] → [3.5mm jack → Arduino A0] → [FFT processing] → [WS2812B LED strip]

Parts needed (~$15 total):
- Arduino Uno (you have it)
- 3.5mm audio jack breakout + 2 resistors (voltage divider)
- WS2812B LED strip (30 pixels)
- 5V 2A power supply
- Wires
```

---

**Ready to go deeper?** Pick a direction and I'll write the code:

1. **FFT frequency bands** — split bass/mids/treble
2. **NeoPixel LED strip** — multiple RGB LEDs
3. **Beat detection** — locked to the rhythm
4. **All of the above** — a full audio visualizer
