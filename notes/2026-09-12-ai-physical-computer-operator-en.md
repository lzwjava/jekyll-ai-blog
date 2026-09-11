---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Physical Computer Operator
translated: false
type: note
---

Question: You’re describing an **AI agent that can operate another physical computer starting from BIOS/UEFI**, by seeing its video output and injecting keyboard input.

Answer: **Yes — exactly.** This is essentially a **hardware-level remote computer control loop**:

```text
                ┌─────────────────────┐
                │      AI Agent       │
                │                     │
                │ vision → reasoning  │
                │ keyboard commands   │
                └─────────┬───────────┘
                          │
                   USB HID keyboard
                          │
                          ▼
┌─────────────────────────────────────────────┐
│             Target Computer                 │
│                                             │
│  BIOS/UEFI → Bootloader → Linux/Windows     │
│      ▲                                      │
│      │ HDMI/DP video                        │
└──────┼──────────────────────────────────────┘
       │
       ▼
 HDMI/DP capture card
       │
       ▼
 AI vision input
```

The important point is that **the agent doesn't need an OS-level API at all**.

At BIOS stage:

```text
AI
 │
 ├── sees BIOS screen through HDMI capture
 │
 ├── decides: "Press F2"
 │
 └── sends USB HID keyboard event
                    │
                    ▼
              BIOS receives F2
```

So this can work even when:

* OS isn't booted
* SSH isn't available
* GPU driver isn't loaded
* NVIDIA driver is broken
* disk is blank
* you're installing an OS
* you're debugging a GPU
* you're sitting at a BIOS/UEFI menu

This is basically **KVM + computer vision + agent**.

### The hardware is surprisingly simple

You need three interfaces:

```text
Target PC HDMI/DP ──→ USB capture ──→ AI computer
                                      │
                                      │ USB
                                      ▼
Target PC USB port ←── HID keyboard device
```

For example, the AI machine could run:

```python
while True:
    frame = capture.read()

    action = agent(frame)

    if action == "F2":
        hid.press("f2")
    elif action == "ENTER":
        hid.press("enter")
    elif action == "UP":
        hid.press("up")
```

The interesting part is that **the keyboard device should enumerate as a normal USB HID keyboard**. The target computer doesn't know or care that an AI is behind it.

For your GPU-repair setup, this is actually quite powerful:

```text
                    AI repair agent
                          │
             ┌────────────┴────────────┐
             │                         │
          video                    keyboard
             │                         │
             ▼                         ▼
       HDMI capture               USB HID
             │                         │
             └──────────┬──────────────┘
                        ▼
                 Test motherboard
                        │
                 ┌──────┴──────┐
                 │             │
              BIOS         Linux/MATS
                 │             │
                 └────── GPU ──┘
```

Then the agent could potentially do the whole sequence:

```text
Power on
  ↓
Observe POST
  ↓
Enter BIOS
  ↓
Select iGPU
  ↓
Boot Debian
  ↓
SSH / terminal
  ↓
Run MODS/MATS
  ↓
Read result
  ↓
Decide next diagnostic step
```

The **BIOS part is the key difference from normal computer-use agents**: you have created an agent that controls the machine **below the operating-system boundary**.

I’d call the architecture:

> **AI-controlled hardware KVM**

or more specifically:

> **Vision → LLM agent → USB HID + HDMI capture**

This is very close to building an **AI technician that can physically operate your GPU test bench**.

I can also sketch the cheapest practical prototype using a USB HDMI capture dongle + Raspberry Pi/ESP32 HID + your 4070 machine.
