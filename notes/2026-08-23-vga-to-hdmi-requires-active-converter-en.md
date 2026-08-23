---
audio: false
generated: true
image: false
lang: en
layout: post
title: VGA to HDMI Requires Active Converter
translated: false
type: note
---

Yes, **VGA to HDMI adapters exist**, but there is an important detail:

* **VGA → HDMI** is **not a simple passive adapter**. VGA is analog; HDMI is digital. You need an **active converter** with a chip inside.

Typical usage:

```
PC / laptop VGA output
        |
        | analog VGA cable
        v
[VGA → HDMI active converter]
        |
        | HDMI cable
        v
Monitor HDMI input
```

Notes:

* It usually needs **USB power** (5V) because conversion requires electronics.
* Supports common resolutions like:

  * 1920×1080 @ 60Hz
  * 1280×720
* Audio:

  * VGA has no audio.
  * Some converters take a 3.5mm audio input and inject it into HDMI.

For your **Lenovo LI2364A monitor** from the previous question:

* If the monitor only has **VGA input**, you need **HDMI → VGA** (opposite direction) from a modern GPU/laptop.
* If your computer only has HDMI/DP and monitor has VGA:

```
GPU HDMI/DP
    |
    v
HDMI → VGA converter
    |
    v
Lenovo VGA port
```

Do not buy a VGA-to-HDMI cable without a converter box; it usually will not work.
