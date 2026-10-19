---
audio: false
generated: true
image: false
lang: en
layout: post
title: Newmine Mic Shows Silence, Not Audio
translated: false
type: note
---

Here's the full picture with all the evidence:

## Test results

| Test | Result |
|---|---|
| **Detection** | ✅ Newmine is visible as a USB audio input device |
| **Capture** | ✅ ffmpeg successfully grabs a stream from it — but it's pure silence |
| **Audio signal** | ❌ **RMS -63 dB / peak -56 dB** — that's digital silence (only a faint noise floor, ~0.0007 DC offset, essentially zero crossings) |
| **Control test** | ✅ Built-in MacBook mic hit **0.0 dB peak** on the same recording — so nothing was wrong with the system or your voice |

So the Newmine is **connected and recognized, but no actual audio is reaching it.** Your voice and the test setup work fine.

## Most likely causes (in order)

1. **Physical mute switch** — most USB/streaming mics have a mute button on the body with an LED. Check if it's lit/muted.
2. **It's a wireless mic** — MUSIC-BOOST (Newmine) tends to be a wireless lavalier set: if the transmitter is **off, unpaired, low-battery, or not switched to the right channel**, the USB receiver outputs exactly this kind of silence.
3. **Input volume slider at 0** — open **System Settings → Sound → Input**, select **Newmine**, and watch the level meter while speaking. If the meter doesn't move, the problem is upstream of macOS.
4. **Bad cable/port** — try another USB port or cable (avoid charging-only hubs).

## Quick check you can do

Go to **System Settings → Sound → Input** and select **Newmine** — then speak. If the orange level meter stays flat, the mic hardware/wireless link is the issue, not software.

Once you've checked the mute switch / transmitter battery / pairing, tell me and I'll re-run the recording test to confirm it's working.
