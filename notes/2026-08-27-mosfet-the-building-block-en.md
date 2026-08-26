---
audio: false
generated: true
image: false
lang: en
layout: post
title: "MOSFET: The Building Block"
translated: false
type: note
---

**Question:** What is a MOSFET?

**Answer:**

---

## 🔬 MOSFET — Metal-Oxide-Semiconductor Field-Effect Transistor

A MOSFET is a **transistor** — the most fundamental building block of modern electronics. It acts as either a **switch** or an **amplifier** controlled by voltage.

---

## 🧱 Physical Structure (What's Inside One)

```
        Gate (G)
          |
  ┌───────┴───────┐
  │   Oxide Layer │  ← insulating SiO₂ (the "oxide")
  │───────────────│
  │  Metal gate   │  ← the "metal" (now usually polysilicon)
  └───────────────┘
  Source (S)     Drain (D)
     │                │
  [N+ region]    [N+ region]
  ───────────────────────────
         P-type silicon body (substrate)
```

Three terminals:
| Terminal | Role |
|---|---|
| **Gate (G)** | The control input — voltage here turns it on/off |
| **Source (S)** | Where current enters (or exits) |
| **Drain (D)** | Where current exits (or enters) |

---

## ⚡ How It Works — The Core Idea

> **Voltage at the Gate controls whether current flows from Drain to Source.**

1. **Gate voltage = LOW (0V)** → no channel forms → transistor **OFF** → no current flows → acts like an **open switch**
2. **Gate voltage = HIGH (e.g. 5V)** → electric field attracts charge carriers → a **conductive channel** forms between Source and Drain → transistor **ON** → current flows → acts like a **closed switch**

The gate is **insulated** from the body by a thin oxide layer, so it draws almost **zero current** to control — very efficient.

---

## 🔁 Two Main Types

| Type | Charge Carriers | Turns ON when Gate is... |
|---|---|---|
| **N-channel (NMOS)** | Electrons | HIGH voltage |
| **P-channel (PMOS)** | Holes | LOW voltage |

In a GPU's VRM, **both types are paired** (called **complementary / half-bridge**) to efficiently push and pull current.

---

## 🎮 What MOSFETs Do in a GPU (like RTX 4070)

In the **VRM (Voltage Regulator Module)**, MOSFETs switch **millions of times per second** (hundreds of kHz) to chop 12V input into precisely regulated lower voltages (e.g. ~1.0V for the GPU core):

```
12V ──► [High-side MOSFET] ──► switch ON/OFF rapidly
                                        ↓
                              [Inductor smooths it]
                                        ↓
                              ~1.0V steady output ──► GPU Die
```

This technique is called **PWM switching** (Pulse Width Modulation). The ratio of ON time vs OFF time determines the output voltage.

---

## 📦 What They Look Like on a PCB

On a GPU board, MOSFETs often appear as:
- Small **black rectangular chips** (DrMOS packages) near the power input area
- Arranged in **rows** next to the chunky inductors (coils)
- They get **hot during load**, which is why GPU coolers also cover this area

---

## 🌍 Scale — MOSFETs in a GPU Die

The RTX 4070's AD104 chip contains roughly **35.8 billion** MOSFETs — each one just **4–5 nanometers** in size, invisible to the naked eye. These are the CUDA cores, cache cells, logic gates — everything inside the chip itself.

So MOSFETs exist at **two scales** on a GPU:
- **Macro scale** — the VRM power transistors you can see (mm-sized)
- **Nano scale** — billions of them etched into the silicon die itself

---

**References:**
- [MOSFET Explained — Electronics Tutorials](https://www.electronics-tutorials.ws/transistor/tran_6.html)
- [How VRMs Work — Gamers Nexus](https://www.gamersnexus.net/guides/voltage-regulator-module-explained)
- [NVIDIA AD104 Die — TechPowerUp GPU Database](https://www.techpowerup.com/gpu-specs/geforce-rtx-4070.c3924)
