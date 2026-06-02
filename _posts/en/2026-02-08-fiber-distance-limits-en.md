---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Fiber Distance Limits Explained Simply
translated: false
type: note
---

Great question! You've spotted the mathematical relationship, but it's important to understand the **different reasons** these distances exist:

**Full-duplex (275m):** This is the practical, real-world maximum distance for reliable bidirectional communication simultaneously. Both directions are transmitting at the same time, and the signal degrades over fiber distance due to attenuation and dispersion. At 275m, the signal quality is still acceptable for error-free transmission in both directions.

**Half-duplex (550m):** This is a theoretical maximum where communication goes in *only one direction at a time*. Since you're only transmitting in one direction, you don't face the same signal degradation challenges from simultaneous bidirectional transmission. The signal can travel farther before becoming unrecoverable.

**Why the 2x difference?**

The relationship isn't purely mathematical—it's more that:

1. **Signal quality degrades with distance** - The fiber attenuates the signal continuously
2. **Full-duplex is twice as demanding** - You're pushing quality-of-service requirements for signals traveling simultaneously in both directions
3. **Half-duplex is more forgiving** - One strong signal can travel farther than trying to maintain two simultaneous signals

Think of it like this: if you're trying to have a phone conversation (full-duplex) versus sending Morse code in one direction only (half-duplex), the one-way signal can be weaker and still be understood.

In practice, **full-duplex is always used in modern networks** because the distance limitation (275m) is usually acceptable for local area applications, and simultaneous bidirectional communication is essential for practical networking.
