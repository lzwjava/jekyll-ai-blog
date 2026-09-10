---
audio: false
generated: true
image: false
lang: en
layout: post
title: Oscilloscope Diagnosis of Power-On Circuit
translated: false
type: note
---

Question: How can you use your oscilloscope to diagnose the **L-IG41M3 motherboard's power-on / power-off circuit**?

Answer: Yes. This is actually a good board to learn oscilloscope-based motherboard repair on. You don't need to probe randomly; follow the **power-state signal chain**.

For your shutdown problem, I would start with these signals:

```text
F_PANEL pin 9
    │
    ▼
PWRBTN_L
    │
    ▼
Super I/O (IT8755E / equivalent)
    │
    ▼
SLP_S3#/SLP_S4#/SLP_S5#
    │
    ▼
ATX_PSON#
    │
    ▼
PSU
```

### 1. First: probe the power-button signal

Set your scope:

```text
Probe:  ×10
Ground: motherboard GND
Coupling: DC
Voltage: 2 V/div
Time:    500 ms/div initially
```

Connect the ground clip to a convenient **GND**, e.g. the metal PSU shield or motherboard ground.

Probe **F_PANEL pin 9**.

With the board powered on, you should see a logic-level signal that changes when you short:

```text
pin 9 ──┐
        │ ← screwdriver
pin 11 ─┘
```

Conceptually:

```text
idle:       ───────────────  HIGH

press:      ────────┐
                    └──────── LOW
                    ~50-500 ms
```

The exact voltage isn't as important initially as seeing **a clean transition**.

If you see this, you have established:

> screwdriver → F_PANEL → PWRBTN input is working.

---

### 2. Then probe the Super I/O response

The interesting part is whether the Super I/O actually reacts to the button.

The L-IG41M3 uses an ITE Super I/O/controller. Around this chip you'll find signals related to:

```text
PWRBTN#
SLP_S3#
SLP_S4#
SLP_S5#
PSON#
```

Don't blindly probe random pins on the IT8755E. **Get the exact schematic/pinout for your board revision first.**

Then use the scope to compare:

```text
             press power button
                    │
                    ▼
PWRBTN#  ───────────┐
                    └───────
                    │
                    ▼
SLP_S5#  ───────────────────┐
                            └────
                    │
                    ▼
ATX_PSON# ──────────────────┐
                            └────
```

The exact polarity depends on the signal (`#` / `_L` generally means active-low).

---

### 3. ATX_PSON# is especially useful

This is probably the **most useful signal for your particular troubleshooting**.

Your ATX PSU has:

```text
PS_ON# 
```

The motherboard controls the PSU through this signal.

Typical behavior:

```text
             OFF / soft-off
PSON#   ───────────── HIGH

             power on
                 ↓
PSON#   ────────┐
                └──────── LOW
```

So find the motherboard's **ATX PSON#** signal and probe it.

Then:

```text
1. Turn board on.
2. Scope PSON#.
3. Short F_PANEL 9 → 11.
4. Watch what happens.
```

If the motherboard successfully processes the shutdown request, you should eventually see **PSON# transition back toward its off-state**.

If:

```text
PWRBTN# changes
        ↓
but
PSON# never changes
```

then you've narrowed the fault substantially to the **motherboard's power-management / Super-I/O / state-control path**, rather than the physical power button.

---

### 4. Use a single-shot capture

For this kind of debugging, don't just stare at a continuously running waveform.

Use:

```text
Trigger:
  Edge
  Source = PWRBTN#
  Falling edge
  Single acquisition
```

Then press the button.

You'll capture something like:

```text
time ─────────────────────────────────────────>

PWRBTN#    ────────────┐________________
                       │
                       │ button press
                       │
SLP_S5#    ────────────────────┐___________
                               │
PSON#      ────────────────────┐____________
                               │
```

Now you can literally see **which stage stops responding**.

---

### 5. Also measure the standby rails

Before doing signal debugging, verify the PSU/motherboard power state.

With PSU connected but PC "off":

```text
Purple wire on 24-pin = +5VSB
```

You should have approximately:

```text
5VSB ≈ 5 V
```

Then probe:

```text
+5VSB
PWRBTN#
PSON#
```

This lets you understand the state machine:

```text
AC connected
     │
     ▼
   +5VSB
     │
     ▼
Super I/O alive
     │
     │ PWRBTN
     ▼
 PSON# asserted
     │
     ▼
 PSU main rails
     │
     ▼
CPU / chipset starts
```

For shutdown:

```text
PWRBTN
   ↓
Super I/O
   ↓
sleep-state logic
   ↓
PSON#
   ↓
PSU main rails OFF
```

---

### 6. One very important oscilloscope safety rule

For this motherboard, **do NOT connect the oscilloscope ground clip to arbitrary power rails.**

Your normal bench scope has earth-referenced ground:

```text
scope ground ─── PE/earth
```

Therefore:

```text
GOOD:
scope GND → motherboard GND

BAD:
scope GND → +12V
scope GND → +5V
scope GND → PSON#
```

The last three can effectively short the signal to earth and potentially damage the board/PSU.

Use **×10 probes** rather than ×1 when possible.

---

### The debugging path I'd use

Since your symptom is:

> **9↔11 can power the board on, but doesn't power it off**

I'd investigate in this order:

```text
① F_PANEL pin 9
       ↓
② PWRBTN# at Super I/O
       ↓
③ Super I/O reacts to button?
       ↓
④ SLP_S3/S4/S5
       ↓
⑤ ATX_PSON#
       ↓
⑥ PSU main rails
```

You don't need to understand the entire motherboard first. **Find the first signal in that chain that doesn't make the expected transition.** That's the oscilloscope's real value in board repair.

If you upload a **clear photo of both sides around the L-IG41M3 F_PANEL + Super I/O + 24-pin ATX area**, I can help you identify practical probe points on *your physical board*.