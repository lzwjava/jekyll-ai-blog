---
audio: false
generated: true
image: false
lang: en
layout: post
title: Oscilloscope Diagnosis for 0.1 Second Fault
translated: false
type: note
---

**Question:** The fan only flickers for 0.1 seconds then shuts down — how do we use an oscilloscope (示波器) to diagnose this problem?

---

**Answer:**

Excellent thinking — an oscilloscope is the **right tool** for this kind of ultra-fast fault diagnosis. Here is how to use it:

---

### 🔬 What is an Oscilloscope Doing Here?A normal multimeter only shows you **current stable voltage**. But when the system dies in **0.1 seconds**, the fault happens so fast a multimeter **cannot catch it**. The oscilloscope records the voltage waveform over time, so you can see exactly:

```
Normal boot:                    Your system:
+12V ─────────────────          +12V ──╮
                                       │ drops instantly
  0V                             0V    ╰──────────────
     time →                           ↑
                                    0.1 sec
```

---

### 📍 Where to Place the Oscilloscope Probes

There are **3 key test points** on the 24-pin ATX connector:

| Pin to Probe | Wire Color | What to Measure | Healthy Value |
|---|---|---|---|
| +12V | Yellow | CPU/main 12V rail | 11.4V – 12.6V |
| +5V | Red | Board logic power | 4.75V – 5.25V |
| +3.3V | Orange | RAM / chipset | 3.135V – 3.465V |
| PS_ON | Green | PSU enable signal | Goes LOW to start |
| PWR_OK | Grey | PSU good signal | Goes HIGH when stable |

**Probe placement:**
```
Black probe (GND) → any BLACK wire on 24-pin
Red probe (+)     → yellow wire (+12V) first
```

---

### 🔧 Step-by-Step Oscilloscope Procedure

**Step 1 — Set up the oscilloscope**
- Time scale: **50ms per division** (so 0.1 sec fits on screen)
- Voltage scale: **5V per division**
- Trigger: set to **falling edge** on +12V channel
- This means it will capture the moment voltage **drops**

---

**Step 2 — Probe the PWR_OK (grey wire) first**

The **PWR_OK signal** is the most important pin for your case:
```
PWR_OK = HIGH (+5V) → PSU says "I am stable, board can run"
PWR_OK = LOW  (0V)  → PSU says "problem detected, shut down"
```

If you see PWR_OK go HIGH then immediately drop LOW within 0.1 seconds — **the PSU is detecting an overcurrent or undervoltage and killing itself.**

---

**Step 3 — Watch the +12V rail during power on**

```
What you want to see:
+12V ────────────────────────────  (stable flat line)

What a failing PSU shows:
+12V ──╮
       ╰──── drops to 8V or less instantly → PSU collapses under load
```

If +12V collapses the moment the CPU tries to draw power → **PSU is too weak or faulty**

---

**Step 4 — Probe the ATX 12V 4-pin (CPU power)**

This is the most critical for your symptom. Probe the yellow wire on the **4-pin CPU connector**:

```
Healthy:   +12V ────────────────
Faulty:    +12V ──╮ drops immediately
                  ╰──── 0V (CPU gets no sustained power)
```

If this line collapses while the main 24-pin +12V stays up → **the PSU cannot deliver enough current through the 4-pin** → PSU is the problem.

---

### 🧭 What the Waveform Tells You

| What Oscilloscope Shows | Conclusion |
|---|---|
| +12V drops immediately on 4-pin | **PSU too weak / failing** |
| PWR_OK never goes HIGH | **PSU dead or overloaded** |
| PWR_OK goes HIGH then drops in 0.1s | **Overcurrent protection triggered** |
| All voltages stable but system dies | **Motherboard or CPU fault** |
| +12V stable, +5V collapses | **PSU 5V rail failing** |
| Everything stable, fan still stops | **Thermal shutdown or bad CPU** |

---

### 💡 For Your Specific 0.1 Second Symptom

The most likely story the oscilloscope will show:

```
t=0ms    → You press power button
t=5ms    → PSU powers up, PWR_OK goes HIGH
t=50ms   → CPU starts drawing current on 4-pin
t=100ms  → +12V rail collapses (Huntkey 280W too weak)
t=100ms  → PWR_OK drops LOW
t=100ms  → Fan stops
```

This would confirm the **Huntkey 280W PSU is the culprit** — it cannot sustain the +12V rail under CPU load.

---

### ⚠️ Safety Notes for Oscilloscope Use

- Always connect **GND probe first** before signal probe
- Never probe **mains voltage (240V wall)** with a standard scope probe
- Keep probes away from the spinning fan
- Use **insulated probe tips** — do not let bare metal touch adjacent pins

---

**References:**
- [Using oscilloscope to diagnose ATX PSU — eevblog.com](https://www.eevblog.com/forum/testgear/using-oscilloscope-to-test-atx-psu/)
- [ATX PSU PWR_OK signal explained — hardwaresecrets.com](https://www.hardwaresecrets.com/everything-you-need-to-know-about-the-atx-power-supply-standard/)
- [How to measure PSU voltages with oscilloscope — electronics.stackexchange.com](https://electronics.stackexchange.com/questions/tagged/power-supply)
