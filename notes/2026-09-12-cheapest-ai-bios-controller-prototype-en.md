---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cheapest AI BIOS Controller Prototype
translated: false
type: note
---

Question: Build the cheapest practical prototype for an **AI agent that can see a PC from BIOS onward and control it via keyboard**, especially for your GPU-repair/test bench.

Answer: I’d build **v1 without a Raspberry Pi**. Your existing 4070 machine can be the AI/controller computer.

```text
                    YOUR 4070 / AI PC
              ┌──────────────────────────┐
              │                          │
 HDMI capture │   Python agent           │
 ────────────►│   ┌──────────────────┐   │
              │   │ screenshot       │   │
              │   │ vision / OCR     │   │
              │   │ LLM reasoning    │   │
              │   │ action selection │   │
              │   └────────┬─────────┘   │
              │            │             │
              │       USB HID            │
              └────────────┼─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ HID device  │
                    │ RP2040      │
                    └──────┬──────┘
                           │ USB
                           ▼
                 ┌───────────────────┐
                 │  TARGET PC        │
                 │                   │
 HDMI OUT ──────►│ BIOS → GRUB → OS  │
                 │       │           │
                 │       ▼           │
                 │     GPU           │
                 └───────────────────┘
```

### 1. Hardware

The minimum BOM is roughly:

| Component                  | Purpose                      |
| -------------------------- | ---------------------------- |
| USB HDMI capture dongle    | Target PC → AI PC            |
| RP2040 / Raspberry Pi Pico | AI PC → fake USB keyboard    |
| HDMI cable                 | Target GPU/iGPU → capture    |
| USB cable                  | RP2040 → target PC           |
| Your existing 4070 PC      | vision + LLM + orchestration |

The **RP2040 is important** because you want the target motherboard to see:

```text
USB device descriptor
    ↓
HID Keyboard
    ↓
BIOS says: "Oh, a keyboard."
```

No target-side software is required.

### 2. Start with deterministic control

Don't put an LLM in the loop immediately.

First prove:

```text
HDMI → screenshot → Python
USB HID → keypress → BIOS
```

For example:

```python
# controller.py

import time
import cv2

cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("capture failed")

    cv2.imshow("target PC", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

Then make the RP2040 behave as a keyboard.

Conceptually:

```python
keyboard.press("f2")
time.sleep(0.1)
keyboard.release("f2")
```

At this point you should be able to physically watch:

```text
AI PC screen
      │
      └── target BIOS
             │
             └── AI PC sends F2
                       │
                       ▼
                   target BIOS
```

### 3. Then add computer vision

Don't send the entire 1920×1080 screenshot to the LLM every 100 ms.

Use a slower agent loop:

```text
capture
   ↓
crop / resize
   ↓
OCR + vision
   ↓
agent
   ↓
action
   ↓
HID
```

Something like:

```python
while True:
    frame = capture()

    observation = vision(frame)

    action = agent(
        observation,
        goal="Set integrated graphics as primary display"
    )

    execute_hid(action)

    time.sleep(0.5)
```

The action space should initially be tiny:

```python
ACTIONS = {
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    "ENTER",
    "ESC",
    "F1",
    "F2",
    "F10",
    "F12",
    "SPACE",
}
```

Don't initially let the model generate arbitrary keyboard scancodes.

### 4. Give the agent a state machine

This is where it becomes much more reliable.

For example:

```text
POWER_ON
   │
   ▼
WAIT_POST
   │
   ├── "Press DEL to enter Setup"
   │
   ▼
BIOS
   │
   ├── find "Advanced"
   ├── find "Graphics"
   ├── find "Primary Display"
   └── select "IGD"
   │
   ▼
SAVE_EXIT
   │
   ▼
BOOT
   │
   ▼
LINUX
   │
   ▼
RUN_MATS
```

The LLM becomes the **planner**, rather than blindly controlling every keypress.

### 5. For your GPU-repair bench, this gets really interesting

You could eventually have:

```text
                 ┌─────────────────┐
                 │    AI Agent     │
                 └────────┬────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
         HDMI vision              USB HID
              │                       │
              ▼                       ▼
       Target motherboard       BIOS keyboard
              │
       ┌──────┴──────┐
       ▼             ▼
     iGPU           NVIDIA GPU
       │             │
       │          MATS/MODS
       │             │
       └──────┬──────┘
              ▼
          test result
              │
              ▼
        AI diagnosis
```

Then your agent can do things like:

```text
"Boot the machine."

"Enter BIOS."

"Enable iGPU."

"Boot Debian."

"Run MATS against GPU #1."

"MATS reports errors on channel X."

"Power off."

"Ask technician to inspect VRAM M5."

```

That is substantially more useful than a generic GUI agent because **the AI has access to the physical machine even before an OS exists**.

### 6. One important upgrade: ATX power control

Eventually I'd add a small microcontroller-controlled relay/ATX interface:

```text
AI
 │
 ├── HDMI capture
 ├── USB HID
 └── power control
          │
          ▼
       ATX PSU
          │
          ▼
      motherboard
```

Then the agent can control the complete lifecycle:

```text
POWER OFF
   ↓
POWER ON
   ↓
POST observation
   ↓
BIOS interaction
   ↓
OS boot
   ↓
MATS
   ↓
shutdown
```

That turns it from **AI computer-use** into something closer to an **AI-controlled hardware test fixture**.

For your current GPU-repair setup, I'd build **v1 with just three things: HDMI capture + RP2040 HID + Python**, prove BIOS control first, and only then connect the vision/LLM layer.
