---
audio: false
generated: true
image: false
lang: en
layout: post
title: Capture HDMI/VGA for AI Vision
translated: false
type: note
---

Question: How do you physically capture **HDMI or VGA output from another PC** so your AI machine can read the BIOS/UEFI screen?

Answer: The key is that **HDMI/VGA are outputs**, so you need a **capture device** that converts the electrical video signal into USB frames your computer can read.

### HDMI — easiest

Use a cheap **USB HDMI capture dongle**:

```text
Target PC
GPU / iGPU HDMI OUT
        │
        │ HDMI
        ▼
┌──────────────────┐
│ HDMI USB Capture │
│                  │
│ HDMI IN → USB    │
└────────┬─────────┘
         │ USB
         ▼
     AI computer
         │
         ▼
 /dev/video0
```

On Linux:

```bash
v4l2-ctl --list-devices
```

You'll typically see something like:

```text
USB Video:
    /dev/video0
```

Then:

```bash
ffplay /dev/video0
```

or Python/OpenCV:

```python
import cv2

cap = cv2.VideoCapture("/dev/video0")

while True:
    ok, frame = cap.read()
    if not ok:
        break

    cv2.imshow("target", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

Now your AI computer is literally receiving the **BIOS pixels as images**.

### VGA is slightly different

VGA is analog RGB:

```text
VGA
 ├── Red
 ├── Green
 ├── Blue
 ├── HSync
 └── VSync
```

You generally don't want to connect VGA directly to a normal USB port.

Use:

```text
Target PC VGA OUT
       │
       ▼
VGA → HDMI converter
       │
       ▼
HDMI capture
       │
       ▼
USB
       │
       ▼
AI PC
```

Or a dedicated:

```text
VGA → USB capture
```

device.

The VGA→HDMI converter performs the important **analog → digital conversion**.

### For your GPU-repair bench

I'd actually standardize on **HDMI** wherever possible:

```text
                    ┌─────────────────────┐
                    │ AI / control PC     │
                    │                     │
                    │ OpenCV              │
                    │ OCR                 │
                    │ VLM                 │
                    │ Agent               │
                    └──────────┬──────────┘
                               │ USB
                         ┌─────▼─────┐
                         │ HDMI      │
                         │ capture   │
                         └─────▲─────┘
                               │ HDMI
                               │
                    ┌──────────┴──────────┐
                    │ Target motherboard  │
                    │                     │
                    │ iGPU / GPU          │
                    └─────────────────────┘
```

You can even have **two target outputs**:

```text
iGPU HDMI ─────┐
               ├── HDMI switch ── capture ── AI
GPU HDMI ──────┘
```

Then the AI can inspect either the motherboard's iGPU output or the discrete GPU output.

### One important BIOS detail

A cheap capture card doesn't necessarily capture **every BIOS signal**.

Some BIOS systems output unusual resolutions/refresh rates, and cheap HDMI capture devices may fail to lock onto them.

For example:

```text
BIOS:
640×480 @ 60
800×600 @ 60
1024×768 @ 60
        ↓
capture device
        ↓
USB UVC 720p/1080p
```

Modern UEFI at 1080p is much easier.

For your **B75/B150 GPU diagnostic machine**, I'd start with a cheap UVC HDMI capture dongle and test:

```bash
v4l2-ctl --list-formats-ext -d /dev/video0
```

Then:

```bash
ffplay -f v4l2 /dev/video0
```

Once this works, the next layer is trivial:

```python
frame = capture.read()
```

and that `frame` becomes the **visual observation fed into your agent**.
