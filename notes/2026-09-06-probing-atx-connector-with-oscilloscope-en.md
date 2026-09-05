---
audio: false
generated: true
image: false
lang: en
layout: post
title: Probing ATX Connector with Oscilloscope
translated: false
type: note
---

**Question:** I have turned on the oscilloscope — where exactly do I put the black probe and red probe?

---

**Answer:**

Good — let's do this carefully step by step.

---

### 🔌 First — What You Are Working With

You have the **24-pin ATX connector** plugged into the motherboard. You will probe it from the **back side** where wires come out — do NOT unplug it.

---

### 📍 Black Probe First (ALWAYS black first — safety rule)

The black probe = **GND (ground)**. Put it on any **black wire** on the 24-pin connector:

```
Find any BLACK wire on the 24-pin bundle
         ↓
Push black probe tip gently alongside
the wire into the back of the connector
         ↓
Or clip it to the metal PC case chassis
(case is also GND — same thing)
```

✅ The **PC case/chassis metal** is the easiest and safest GND point — just clip the black probe crocodile clip onto any unpainted metal part of the case.

---

### 📍 Red Probe — Start With PWR_OK (Grey Wire)

For your symptom (fan flickers 0.1 sec), the **most useful first measurement** is the **PWR_OK pin** — grey wire on the 24-pin:

---

### 🗺️ 24-pin Connector Pin Map

Here is where to find each wire looking at the **back of the connector** (where wires come out):

```
LOOKING AT BACK OF 24-PIN (wire side)

Row 1:  [3.3V] [3.3V] [GND] [+5V] [GND] [+5V] [GND] [PWR_OK] [5VSB] [+12V] [+12V] [GND]
color:  [ORG]  [ORG]  [BLK] [RED] [BLK] [RED] [BLK]  [GREY]  [PURP] [YEL]  [YEL]  [BLK]

Row 2:  [3.3V] [-12V] [GND] [PS_ON] [GND] [GND] [GND] [-5V] [+5V] [+5V] [+5V] [GND]
color:  [ORG]  [BLU]  [BLK] [GRN]   [BLK] [BLK] [BLK] [WHT] [RED] [RED] [RED] [BLK]
```

---

### 🎯 Probe Sequence — Do in This Order

**Measurement 1 — PWR_OK (most important for your case)**

```
Black probe → PC case metal (GND)
Red probe   → GREY wire (PWR_OK)
```

Watch what happens when you press power:

- Goes to +5V then drops instantly = **PSU protection triggered**
- Never goes up at all = **PSU is dead**

---

**Measurement 2 — +12V main rail**

```
Black probe → PC case metal (GND)
Red probe   → YELLOW wire on 24-pin
```

Watch if +12V collapses when fan kicks then dies

---

**Measurement 3 — +12V CPU rail (4-pin ATX12V)**

```
Black probe → PC case metal (GND)
Red probe   → YELLOW wire on the small 4-pin CPU connector
```

This is the most critical for CPU power delivery

---

### ⚠️ Important Rules

| Rule | Reason |
| --- | --- |
| **Always connect BLACK first** | Safety — establishes ground reference |
| **Never probe green wire (PS_ON) with power on** | Can accidentally force PSU on/off |
| **Do not let red probe tip touch two pins at once** | Will cause a short circuit |
| **Keep probes away from fan blades** | Safety |

---

### 🖥️ Oscilloscope Settings to Set Now

Before pressing power button:

```
Time/div  → 50ms  (so 0.1 sec = 2 divisions on screen)
Volt/div  → 5V    (so +12V appears near top of screen)
Trigger   → EDGE, FALLING, on CH1
Trigger level → set to about 6V
```

This way the scope will **automatically capture** the moment voltage drops — even if it happens in 0.1 seconds.

---

**Press power button → watch the screen → tell me what you see on the waveform.**

---

**References:**

- [ATX 24-pin pinout diagram — pinouts.ru](https://pinouts.ru/Power/atxpower_pinout.shtml)
- [How to use oscilloscope probes safely — Tektronix](https://www.tek.com/en/documents/primer/oscilloscope-probe-guide)
- [Diagnosing PSU with oscilloscope — eevblog.com](https://www.eevblog.com/forum/testgear/using-oscilloscope-to-test-atx-psu/)
