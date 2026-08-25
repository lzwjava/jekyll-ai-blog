---
audio: false
generated: true
image: false
lang: en
layout: post
title: Front Audio 10-Pin Explained
translated: false
type: note
---

**Question:** Why does the front audio (F_AUDIO) header on a motherboard have 10 pins?

**Answer:**

The front audio header uses a **10-pin layout (technically 9 pins + 1 blank/key)** for the following reasons:

**Signal requirements (what the pins carry):**

| Pin | Function |
|-----|----------|
| 1 | MIC2_L (Mic Left) |
| 2 | GND |
| 3 | MIC2_R (Mic Right) |
| 4 | −ACZ_DET (Audio Codec Detect) |
| 5 | LINE2_R (Headphone Right) |
| 6 | FAUDIO_JD (Jack Detection) |
| 7 | FAUDIO_GND |
| 8 | **KEY (physically blocked — missing pin)** |
| 9 | LINE2_L (Headphone Left) |
| 10 | FAUDIO_JD (second jack detect) |

**Why 10 and not fewer?**

- The connector needs to carry two separate audio signals — headphone output and microphone input — along with their respective ground references.

- HD Audio also includes **jack detection sensor pins** — these extra pins tell the system when a plug has been physically inserted into the front jack, which is what allows auto-switching between front and rear audio. This is what the older AC'97 standard (7-pin) lacked.

- **Pin 8 is physically absent (the "key pin")** — its only job is to prevent you from inserting the cable backwards or offset, acting as an idiot-proof alignment guide.

**In short:** The 10-pin design (Intel HD Audio standard) accommodates stereo headphone out + stereo mic in + ground wires + jack detection signals, all while using pin 8 as a physical key to prevent wrong insertion.

**References:**
- [AAFP Connector Explained — CGDirector](https://www.cgdirector.com/aafp-connector-on-motherboard/)
- [What is AAFP on Motherboard — SunbeamTech](https://sunbeamtech.com/hardware-guides/what-is-aafp-on-motherboard/)
- [Front Panel Connectors Complete Pinout Reference — LCSC](https://www.lcsc.com/blog/front-panel-connectors-complete-pinout-reference-for-engineers-systems-builders/)
