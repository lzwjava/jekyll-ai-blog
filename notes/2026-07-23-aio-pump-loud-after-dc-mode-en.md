---
audio: false
generated: true
image: false
lang: en
layout: post
title: AIO Pump Loud After DC Mode
translated: false
type: note
---

Sorry about that. Let me answer in English.

## Why it's still loud after switching AIO_PUMP to DC Mode

**Switching to DC mode only changes the control method, not the speed curve.** The motherboard still applies a variable voltage based on the CPU temperature curve. DC mode just means voltage-based control instead of PWM signal — the curve is still active.

### The fix: flatten the fan curve

Enter BIOS → **Hardware Monitor** / **Fan Settings** → find **AIO_PUMP**:

**Option A (recommended): Switch back to PWM, then set curve to 100% flat**

| Temperature | 30°C | 40°C | 60°C | 70°C | 80°C |
|-------------|------|------|------|------|------|
| **Speed**   | 100% | 100% | 100% | 100% | 100% |

This keeps the pump at full constant speed regardless of CPU temp. Water flow is steady, no temperature oscillation.

**Option B: Keep DC mode, but flatten the curve the same way** — all points at 100%.

---

### But the real noise might be the **radiator fans**

You mentioned you moved fans around. Where are the **radiator fan cables** plugged in now?

- If they're plugged into a **SYS_FAN** header or are running at uncontrolled full speed, that's likely your noise source.
- If you didn't reconnect them properly, they might be running at 100% all the time.

### What to check

| Header | Cable | Mode | Curve |
|--------|-------|------|-------|
| **AIO_PUMP** | Pump cable (from pump block) | **PWM** | **100% all points** (constant speed) |
| **CPU_FAN** | Radiator fans (via splitter) | PWM | Default or adjusted to your liking |

**The radiator fans** should go to **CPU_FAN** — that way they respond to CPU temp and slow down when idle. If they're on SYS_FAN with a different curve, they might be running faster than needed.

Can you tell me which physical headers your two cables (pump vs fans) are plugged into right now?
