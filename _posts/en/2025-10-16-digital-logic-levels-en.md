---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Digital Circuit Logic Levels Explained
translated: false
type: note
---

Yes, that's a solid analogy! In digital circuits like the SR flip-flop, "high" (logic 1) and "low" (logic 0) refer to voltage levels on the wires or signals.

- **High (1)**: A voltage that's sufficiently positive, often around 3.3V, 5V, or even higher (like your 4V battery example) depending on the circuit family (e.g., TTL logic uses ~5V as high). It's enough to represent an "on" or "true" state.
- **Low (0)**: Near ground potential, basically 0V (or very close to it), like the 0V in your battery setup, meaning "off" or "false."

These aren't super precise—there's a small "fuzzy" range in between where the signal might not be reliably read as high or low—but in practice, it's binary: powered up = 1, powered down = 0. For the SR flip-flop, applying a high voltage to the S input sets Q to high (1), just like flipping a switch to "on."
