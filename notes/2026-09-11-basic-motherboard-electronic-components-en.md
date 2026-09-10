---
audio: false
generated: true
image: false
lang: en
layout: post
title: Basic Motherboard Electronic Components
translated: false
type: note
---

Question: What are the basic electronic components you’ll find on a computer motherboard?

Answer: A motherboard is basically a **large power-distribution + signal-routing + control circuit**. The main component families are:

| Component                      | Symbol / typical appearance               | Main job                                                                   |
| ------------------------------ | ----------------------------------------- | -------------------------------------------------------------------------- |
| **Resistor (R)**               | Tiny rectangular SMD                      | Limits current, voltage division, pull-up/pull-down, sensing               |
| **Capacitor (C)**              | Tiny ceramic blocks / larger polymer cans | Stores charge, filtering, decoupling, smoothing                            |
| **Inductor / choke (L)**       | Coils or square power inductors           | Stores magnetic energy, filters/smooths power                              |
| **Diode (D)**                  | Small SMD                                 | Allows current mainly one direction, protection/clamping                   |
| **MOSFET**                     | 6–8 pin SMD packages                      | High-speed electronic switch; used heavily in VRMs                         |
| **IC / chip**                  | Black packages with many pins             | Performs complex functions: CPU power control, USB, audio, LAN, BIOS, etc. |
| **Crystal / oscillator (Y/X)** | Small metal/ceramic package               | Provides precise clock frequency                                           |
| **Transformer**                | Larger magnetic component                 | Isolation/conversion, especially in Ethernet/power circuits                |
| **Fuse (F)**                   | Small SMD component                       | Protects against excessive current                                         |
| **TVS diode**                  | Usually near ports                        | Surge/ESD protection                                                       |
| **Thermistor (NTC/PTC)**       | Resistor-like                             | Temperature/current-related sensing or protection                          |
| **LED**                        | Tiny light-emitting component             | Status/debug indication                                                    |
| **Connector**                  | USB, DIMM, PCIe, ATX, etc.                | Mechanical/electrical interface                                            |

### 1. Capacitors — probably the most numerous

On a motherboard you'll see **hundreds or thousands of MLCCs**:

```text
        VCC
         │
        ┌┴┐
        │C│  ← capacitor
        └┬┘
         │
        GND
```

Their most important motherboard job is **decoupling**.

For example, a CPU suddenly demands more current:

```text
VRM ──────── CPU
 │           │
 └── C ──────┘
     │
    GND
```

The capacitor provides a tiny local energy reservoir and, importantly, gives high-frequency current a short path. This helps keep the CPU supply voltage stable.

---

### 2. Resistors

A resistor might look almost indistinguishable from a capacitor:

```text
 ──[ R ]──
```

Typical uses:

```text
3.3V
 │
[R]  ← pull-up
 │
 ├──── signal
 │
IC
```

They are also used for:

* voltage sensing
* current sensing
* setting IC operating parameters
* termination
* pull-up/pull-down
* configuring PCIe/USB/etc.

---

### 3. Inductors

These become extremely important when you start looking at **GPU/motherboard power circuits**.

A typical CPU VRM is approximately:

```text
12V
 │
MOSFET
 │
MOSFET
 │
 L  ← power inductor
 │
 ├──────── CPU Vcore
 │
 C
 │
GND
```

The **MOSFETs switch** rapidly, the **inductor stores/transfers energy**, and the **capacitors smooth the resulting voltage**.

That's essentially the core of a buck converter.

---

### 4. MOSFETs

Think of a MOSFET as an electrically controlled switch:

```text
        Drain
          │
       ┌──┴──┐
Gate ──┤MOSFET├
       └──┬──┘
          │
        Source
```

On motherboards they're everywhere:

* CPU VRM
* RAM power
* chipset power
* GPU power
* USB power switching
* power sequencing
* load switches

For repair, MOSFETs are particularly important because a shorted MOSFET can cause something like:

```text
12V ── MOSFET ──> GND
```

which can make a power rail effectively short to ground.

---

### 5. Diodes

A basic diode:

```text
──|>|──
```

Current preferentially flows one direction.

Motherboards use different types for:

* ESD protection
* over-voltage protection
* reverse-polarity protection
* voltage clamping
* power conversion

**TVS diodes** are especially common around external connectors such as USB.

---

### 6. ICs

These are the "brains" of the supporting circuitry.

A motherboard can contain ICs for:

```text
CPU
 │
 ├── VRM controller
 ├── chipset / PCH
 ├── Super I/O
 ├── audio codec
 ├── Ethernet controller
 ├── USB controllers
 ├── clock generator
 ├── EC
 ├── BIOS/flash
 └── monitoring/sensor ICs
```

For example, a VRM controller doesn't provide the power itself. It **controls MOSFET switching** according to feedback:

```text
                 ┌─────────────┐
12V → MOSFETs → L → CPU Vcore  │
       ↑             │          │
       │             └──feedback│
       │                        ↓
       └──────── VRM controller
```

This is a very useful mental model for motherboard/GPU repair.

### The big picture

If you're learning board repair, I'd learn the components in roughly this order:

**resistor → capacitor → diode → MOSFET → inductor → buck converter/VRM → IC → buses/signals**

Once you understand **R, C, diode, MOSFET + inductor**, a huge amount of motherboard circuitry stops looking like random tiny components and starts looking like recognizable circuits.

I can also build you a **"motherboard component → multimeter measurement → normal/faulty reading" cheat sheet**, which is probably the most useful next step for your GPU/board repair work.
