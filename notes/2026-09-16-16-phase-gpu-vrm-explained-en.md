---
audio: false
generated: true
image: false
lang: en
layout: post
title: 16-Phase GPU VRM Explained
translated: false
type: note
---

**Question:** What does “16-phase” mean in a GPU VRM, and why use 16 phases?

**Answer:**

Think of the GPU VRM as **16 little buck converters working in parallel**, all feeding the same GPU core voltage rail.

A simplified single phase looks like:

```text
             12V
              │
          ┌───▼───┐
          │ MOSFET│  ← switches at high frequency
          └───┬───┘
              │
           ┌──▼──┐
           │     │
           │ L   │  ← inductor
           │     │
           └──┬──┘
              │
              ├────────── GPU Vcore ≈ 0.8~1.0V
              │
            caps
              │
             GND
```

A **16-phase** design is roughly:

```text
                    ┌─ Phase 0 ─ MOSFET ─ L ─┐
                    ├─ Phase 1 ─ MOSFET ─ L ─┤
12V ────────────────┼─ Phase 2 ─ MOSFET ─ L ─┼─── Vcore
                    │          ...            │
                    └─ Phase15 ─ MOSFET ─ L ─┘

                         ↑
                     uP9512U
                    PWM controller
```

The phases are **interleaved in time**. They aren't 16 independent voltages; they're 16 synchronized power stages sharing one output rail. Multiphase VRMs use this arrangement to distribute current and reduce output ripple. ([Cadence PCB Resources][1])

### Why not just one giant converter?

Suppose the GPU needs:

```text
V = 0.9 V
I = 400 A

P ≈ 0.9 × 400 = 360 W
```

With one phase, that entire **400 A** goes through one set of power components.

With 16 phases, ideally:

```text
400 A / 16 = 25 A per phase
```

So each phase might look conceptually like:

```text
Phase 0:   25A ─┐
Phase 1:   25A ─┤
Phase 2:   25A ─┤
   ...           ├── 400A total
Phase15:   25A ─┘
```

This dramatically helps with:

1. **Current handling** — each MOSFET/inductor handles less current.
2. **Thermals** — conduction loss roughly follows `I²R`, so distributing current matters enormously.
3. **Transient response** — many phases can respond to rapid GPU load changes.
4. **Ripple** — phases are offset from each other, so their ripple partially cancels. ([VoltGround][2])

---

### But what does "phase" actually mean electrically?

This is the interesting part.

Suppose each phase switches at:

```text
f_sw = 500 kHz
```

With 4 phases, you can stagger them:

```text
Phase 0: |████|        |████|
Phase 1:     |████|        |████|
Phase 2:         |████|        |████|
Phase 3:             |████|        |████|
```

For 16 phases:

```text
P0   ↑
P1     ↑
P2       ↑
P3         ↑
...
P15                            ↑
```

They're separated by approximately:

$$
\frac{360^\circ}{16}=22.5^\circ
$$

So although every phase individually switches at 500 kHz, the combined output has much more frequent ripple cancellation.

That's why **"16 phases" doesn't mean 16× the switching frequency**. Each converter still switches at its own switching frequency; the phases are **time-interleaved**.

---

### Why exactly 16?

There isn't anything magical about 16.

It's an engineering tradeoff.

For a high-end GPU:

```text
             fewer phases
                  │
                  ▼
        ┌──────────────────┐
        │  4 phases        │
        │  100 A each      │
        └──────────────────┘
                  │
                  │
        ┌──────────────────┐
        │  8 phases        │
        │   50 A each      │
        └──────────────────┘
                  │
                  │
        ┌──────────────────┐
        │ 16 phases        │
        │   25 A each      │
        └──────────────────┘
```

More phases generally mean **more components, PCB area, cost, gate-drive losses and control complexity**. So you don't keep adding phases forever. ([AI Data Centers][3])

And importantly, **16 phases isn't automatically better than 12 phases**. The actual power-stage current rating, MOSFET/DrMOS efficiency, inductors, switching frequency, thermal design, PCB copper, and controller implementation all matter.

---

### One interesting detail about your uP9512U

The uP9512 family is specifically a **multiphase GPU buck controller**. Its datasheet describes phase current sensing and current balancing across the phases. It can also dynamically reduce the number of active phases at lighter loads ("phase shedding"). ([UPI Semi][4])

So conceptually:

```text
GPU idle
   ↓
maybe 2~4 phases active
   ↓
GPU load increases
   ↓
8 phases
   ↓
heavy load
   ↓
16 phases
```

The exact number depends on the particular uP9512 variant/board implementation—the original uP9512 documentation itself specifies selectable 1–8 phase operation, so if your board is advertised as **16-phase**, there is likely additional phase-doubling/interleaving circuitry or a related controller implementation involved. ([Alldatasheet][5])

**The mental model I'd keep is simply:**

```text
"16-phase VRM"
       =
"16 parallel little buck converters
 sharing the GPU's enormous current,
 with their switching clocks staggered."
```

If you're reverse-engineering an actual GPU PCB, I can also walk through **how to look at the board and identify the 16 phases from the inductors, DrMOS/MOSFETs, PWM traces, and uP9512 pins**.

[1]: https://resources.pcb.cadence.com/pcb-design-blog/2019-what-is-a-vrm-and-why-does-my-cpu-gpu-need-one-2?utm_source=chatgpt.com "What is a VRM and Why Does My CPU/GPU Need One? | Advanced PCB Design Blog | Cadence"
[2]: https://voltground.com/hardware/gpu-vrm-phases-power-delivery/?utm_source=chatgpt.com "GPU VRM Phases and Power Delivery: What Phase Count Actually Means for Overclocking — VoltGround"
[3]: https://aidatacenterguide.com/part-7-compute-silicon-and-system-integration/7-12-on-package-power-delivery-and-power-integrity?utm_source=chatgpt.com "On-Package Power Delivery & Power Integrity · The Definitive Guide to AI Data Centers"
[4]: https://www.upi-semi.com/upisemi/products/ic/dc-dc-controller/multiple-phase-buck-controller/up9512p/?utm_source=chatgpt.com "uP9512P | uPI Semi"
[5]: https://www.alldatasheet.net/html-pdf/2289152/UPI/UP9512/61/1/UP9512.html?utm_source=chatgpt.com "UP9512 datasheet(1/31 Pages) UPI | 8/7/6/5/4/3/2/1-Phase Synchronous-Rectified Buck Controller with SMBus Digital Interface"
