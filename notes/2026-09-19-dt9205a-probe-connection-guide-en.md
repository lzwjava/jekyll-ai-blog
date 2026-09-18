---
audio: false
generated: true
image: false
lang: en
layout: post
title: DT9205A+ Probe Connection Guide
translated: false
type: note
---

**Question:** On the Baolian DT9205A+ multimeter, how should the black and red probes be connected to the COM, V, and Ω ports at the bottom of the meter?

**Answer:**

The DT9205A+ has **4 input jacks** at the bottom. Here's how to connect the probes:

---

### 🔴 Red Probe

| Measurement | Insert Red Probe Into |
| --- | --- |
| Voltage (V AC/DC) | **VΩmA** jack |
| Resistance (Ω) | **VΩmA** jack |
| Current ≤200mA | **VΩmA** jack |
| Current >200mA (up to 20A) | **20A** jack |

---

### ⚫ Black Probe

| Measurement | Insert Black Probe Into |
|---|---|
| **All measurements** | **COM** jack (always) |

---

### Port Layout (bottom of meter, left → right)

```
[ 20A ]  [ mA ]  [ COM ]  [ VΩmA ]
```

| Jack | Color | Purpose |
| --- | --- | --- |
| **COM** | Black ⚫ | Common / Ground — black probe **always** goes here |
| **VΩmA** | Red 🔴 | Voltage, Resistance (Ω), and small current |
| **mA** | Red 🔴 | Milliamp current only (if model has separate mA jack) |
| **20A** | Red 🔴 | High current (up to 20A) only |

---

### ✅ For everyday use (V and Ω)

- **Black probe → COM**
- **Red probe → VΩmA**

> ⚠️ **Warning:** Never plug the red probe into the **20A** jack when measuring voltage or resistance — this will short-circuit the circuit and may damage the meter or cause injury.

---

**References:**

- [DT9205A+ Digital Multimeter User Manual (PDF)](https://www.manualslib.com/manual/dt9205a/)
- [How to Use a Multimeter – Probe Connection Guide](https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-use-a-digital-multimeter)
