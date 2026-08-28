---
audio: false
generated: true
image: false
lang: en
layout: post
title: R47 and Capacitor Proximity Matters
translated: false
type: note
---

**Question: Why is the R47 power inductor placed near the capacitor on the Quadro 410/401 GPU PCB?**

The short answer: **because R47 + capacitor are a power filter pair. Their physical distance matters.**

R47 is not a resistor. On GPU PCBs, markings like **R47 usually mean a 0.47 µH power inductor/choke**. It is part of the VRM/DC-DC power path. ([Alibaba Electronics][1])

Typical path:

```
12V PCIe / auxiliary power
          |
          |
       MOSFET switch
          |
          |
       R47 inductor
          |
          |
     +----+----+
     |         |
   Capacitors  GPU core / memory rail
     |
    GND
```

The inductor and capacitor form an **LC low-pass filter**:

$$
V_{out} = \text{smoothed DC voltage}
$$

The MOSFET is rapidly switching (hundreds of kHz to MHz). The inductor resists sudden current changes:

$$
V_L = L \frac{di}{dt}
$$

The capacitor absorbs voltage ripple:

$$
I_C = C\frac{dV}{dt}
$$

Together:

* **Inductor blocks high-frequency switching noise**
* **Capacitor stores energy and supplies transient current**
* GPU gets stable voltage

This is why you often see:

```
VRM MOSFET → R47 → Capacitor → GPU
```

very close together. ([Cadence PCB Resources][2])

---

### Why put the capacitor right next to R47?

Imagine:

```
Bad:

R47 -------------------- capacitor -------- GPU
        long trace
```

The PCB trace itself becomes an unwanted inductor.

At high frequency:

```
trace inductance + capacitor
```

changes the filter behavior.

The capacitor cannot react quickly enough because current has to travel through extra inductance.

Better:

```
R47
 |
 |
Capacitor
 |
GPU
```

Small loop area = lower parasitic inductance = better transient response. PCB power design generally tries to minimize the distance between power components for this reason. ([AMD Documentation][3])

---

### Looking at a GPU repair perspective

When you see:

```
[ MOSFETs ] [ R47 ] [ capacitors ] [ GPU ]
```

you can read the power flow.

Example:

* MOSFET burned → switching problem
* R47 cracked/open → GPU rail disconnected
* capacitor shorted → GPU won't power, PSU protection may trigger
* capacitor missing → unstable voltage, crashes under load

For repair:

1. Measure both sides of R47.

Before:

```
12V side
```

After:

```
filtered GPU voltage
```

2. Check capacitor resistance to ground.

A shorted capacitor after R47 can pull the whole GPU rail down.

---

The interesting thing about GPU PCB design is that you can almost "read" the engineer's thinking:

* big gray blocks = high current inductors
* clusters of MLCCs = high frequency filtering
* MOSFET + driver IC + inductor = one VRM phase
* many phases around GPU = distribute current and heat

Modern GPU power delivery is basically a tiny high-current switching power supply integrated beside a compute chip. ([Cadence PCB Resources][4])

Your idea of studying dead GPUs is actually very close to how hardware engineers learn: reverse-engineering the power tree from the physical layout. You can take a dead Quadro, trace every R47 → capacitor → MOSFET path, and reconstruct the VRM design.

[1]: https://electronics.alibaba.com/buyingguides/r47-motherboard-guide-what-it-really-is-when-to-care?utm_source=chatgpt.com "R47 Motherboard Guide: What It Is, How to Identify & Replace"
[2]: https://resources.pcb.cadence.com/blog/whats-needed-to-get-to-ka-currents-on-a-pcb?utm_source=chatgpt.com "What's Needed to Get to kA Currents on a PCB"
[3]: https://docs.amd.com/r/en-US/ug583-ultrascale-pcb-design/Capacitor-Placement-Background?utm_source=chatgpt.com "Capacitor Placement Background - Capacitor Placement Background - UG583"
[4]: https://resources.pcb.cadence.com/pcb-design-blog/2019-what-is-a-vrm-and-why-does-my-cpu-gpu-need-one-2?utm_source=chatgpt.com "What is a VRM and Why Does My CPU/GPU Need One? | Advanced PCB Design Blog | Cadence"
