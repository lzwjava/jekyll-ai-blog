---
audio: false
generated: true
image: false
lang: en
layout: post
title: "HDMI Over Long Distances: Solutions"
translated: false
type: note
---

**Question:** Can an HP ZBook laptop maintain a stable HDMI signal over a 50-meter extended cable?

**Answer:**

No — standard passive HDMI cables will not reliably work at 50 meters. Here's the signal physics breakdown:

## HDMI Signal Attenuation Limits

HDMI uses TMDS (Transition-Minimized Differential Signaling) — a high-frequency differential signal. The spec limits are:

| HDMI Version | Max passive cable length |
|---|---|
| HDMI 1.4 (1080p) | ~15 meters |
| HDMI 2.0 (4K@60) | ~10 meters |
| HDMI 2.1 (8K) | ~3–5 meters |

At 50m passive, you will get: dropped frames, signal dropouts, no signal at all, or HDCP handshake failures.

## Solutions That Actually Work at 50m

### 1. Active HDMI Cable (cheapest fix)
Active cables have built-in signal boosters/equalizers at each end. Brands like Monoprice, Cable Matters make 50m active HDMI cables. Around $30–80. Works for 1080p/4K depending on the cable. **This is the easiest drop-in solution.**

### 2. HDMI over Fiber (best signal integrity)
Fiber optic HDMI cables (also called AOC — Active Optical Cable) convert HDMI to optical signal, run over fiber, and convert back. Zero attenuation at 50m. Supports 4K@60 easily. Around $50–150 for 50m.

### 3. HDMI Extender over Cat5e/Cat6 (most common in AV installs)
Uses a TX/RX balun pair, sends HDMI over Ethernet cable. Very common in conference rooms and pro AV. Supports up to 70–100m at 1080p, 40–50m at 4K. Around $20–60 for a kit. Requires a power source at the receiver end.

### 4. HDMI over IP (most flexible, overkill for single display)
Encode HDMI to H.264/H.265, transmit over LAN, decode at the display. Latency is an issue for interactive use.

## For an HP ZBook Specifically

ZBooks often have **USB-C/Thunderbolt** ports — you can use a USB-C to HDMI adapter at the laptop end and then run any of the above. No issues there.

**Recommended for your use case:** Get a **50m Active Optical HDMI Cable (AOC)** — one cable, no external power needed at the display end, 4K capable, and completely transparent to the OS.