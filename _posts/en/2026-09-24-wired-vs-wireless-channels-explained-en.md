---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wired vs Wireless Channels Explained
translated: false
type: note
---

**Question:** What is a 信道 (channel), and what are the differences between 有线信道 (wired channels) and 无线信道 (wireless channels)?

**Answer:**

A **信道 (channel)** is the medium or pathway through which a signal travels from a transmitter to a receiver. It is the physical or logical link that carries information in a communication system. Every channel has characteristics that affect signal quality — including bandwidth, noise, attenuation, and delay.

---

### 有线信道 (Wired Channels)

Wired channels use a physical conductor to guide the signal. The three main types are:

**双绞线 (Twisted Pair):** Two insulated copper wires twisted together to reduce electromagnetic interference (EMI). Common in telephone lines and Ethernet (Cat5/Cat6). Cost-effective but limited in bandwidth and distance.

**同轴电缆 (Coaxial Cable):** A central conductor surrounded by insulation, a metallic shield, and an outer jacket. Better noise immunity than twisted pair; used in cable TV and older Ethernet.

**光纤 (Optical Fiber):** Uses light pulses through glass or plastic fiber. Extremely high bandwidth, immune to EMI, low attenuation over long distances — the backbone of modern internet infrastructure.

---

### 无线信道 (Wireless Channels)

Wireless channels use the electromagnetic spectrum (radio waves, microwaves, infrared, etc.) to carry signals through free space. Unlike wired channels, they are shared, unguided, and much more susceptible to environmental effects.

Key impairments unique to wireless:

- **多径衰落 (Multipath Fading):** Signals bounce off buildings, mountains, and objects, arriving at the receiver via multiple paths with different delays — causing constructive or destructive interference.
- **阴影效应 (Shadowing):** Large obstacles (hills, buildings) block signals and create "shadow zones."
- **多普勒效应 (Doppler Effect):** When the transmitter or receiver is moving, the signal frequency shifts, causing distortion.
- **干扰 (Interference):** Since the spectrum is shared, signals from other transmitters can interfere.

Common wireless channel types include: terrestrial radio (AM/FM, cellular), microwave links, satellite channels, and infrared (short range, like TV remotes).

---

Here's a visual comparison:---

### Key Comparison

| Feature | 有线 Wired | 无线 Wireless |
| --- | --- | --- |
| Medium | Physical conductor | Electromagnetic waves |
| Mobility | Fixed | Mobile |
| Bandwidth | Very high (fiber) | Limited by spectrum |
| Interference | Low | High (shared spectrum) |
| Deployment cost | High (cabling) | Lower for wide area |
| Main impairment | Attenuation | Fading, multipath, Doppler |

Click any box in the diagram above to explore further. You can also ask about specific subtopics like multipath fading models (Rayleigh, Rician), OFDM for handling multipath, or fiber optic transmission principles.
