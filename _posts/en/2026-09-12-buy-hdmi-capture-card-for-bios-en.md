---
audio: false
generated: true
image: false
lang: en
layout: post
title: Buy HDMI Capture Card for BIOS
translated: false
type: note
---

Question: What should you search for on JD.com to buy the HDMI capture device for your AI-controlled BIOS machine?

Answer: The Chinese name is **HDMI 视频采集卡**. For your use case, search these exact terms:

```text
HDMI 视频采集卡 USB
HDMI 转 USB 采集卡
USB3.0 HDMI 视频采集卡
UVC HDMI 视频采集卡
HDMI 采集卡 1080P 60Hz
```

JD currently has many products explicitly described as **“HDMI视频采集卡…转USB”** and **UVC** capture devices. ([JD.com][1])

### What I'd buy

For your BIOS/GPU-repair project, **don't pay for a 4K professional capture card**. You don't need 4K.

Look for:

```text
HDMI IN
    ↓
USB 3.0
    ↓
UVC
    ↓
1080p60
```

Ideally the listing says:

> **USB 3.0 HDMI 视频采集卡，1080P 60Hz，UVC免驱**

The critical word is **UVC**. That means Linux/macOS/Windows can generally treat it like a standard USB video device rather than requiring proprietary software.

JD has, for example, UGREEN models offering HDMI input → USB/Type-C capture, including 1080p60 variants. ([JD.com][2])

### Don't confuse these two

**You want:**

```text
HDMI OUT ──► [ HDMI 视频采集卡 ] ──USB──► AI PC
```

**NOT:**

```text
USB ──► HDMI OUT
```

The latter is a USB-to-HDMI display adapter and is the opposite direction.

### For your first prototype

I'd search JD for:

```text
USB3.0 HDMI采集卡 1080P60 UVC 免驱
```

and pick a **¥50–150-ish generic/UVC unit** rather than an expensive professional card.

The AI doesn't care whether the capture card costs ¥50 or ¥500. What matters is that Linux gives you something like:

```bash
/dev/video0
```

Then:

```bash
v4l2-ctl --list-devices
ffplay /dev/video0
```

and you have the BIOS pixels available to your agent.

If you want, **send me 2–3 JD listings/screenshots you find**, and I can tell you which one is actually suitable for BIOS capture rather than just marketing as a “4K capture card.”

References:

* [JD.com UVC capture-card search](https://www.jd.com/hprm/670ea21d4c988274b9d.html?utm_source=chatgpt.com)
* [JD.com UVC capture-card brands/models](https://www.jd.com/brand/670ea21d4c988274b9d.html?utm_source=chatgpt.com)

[1]: https://www.jd.com/hprm/670ea21d4c988274b9d.html?utm_source=chatgpt.com "uvc采集卡 - 京东"
[2]: https://www.jd.com/hprm/670ea21d4c988274b9d.html?brand=%E7%BB%BF%E8%81%94%EF%BC%88UGREEN%EF%BC%89&electedExtAttrSet=&extAttrValue=expand_name%2C&sort_type=sort_default&utm_source=chatgpt.com "uvc采集卡 - 京东"
