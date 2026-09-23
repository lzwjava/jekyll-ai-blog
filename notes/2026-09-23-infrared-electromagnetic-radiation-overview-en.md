---
audio: false
generated: true
image: false
lang: en
layout: post
title: Infrared Electromagnetic Radiation Overview
translated: false
type: note
---

Question: What is **红外线电磁波 (infrared electromagnetic radiation)**?

Answer:

**Infrared (IR) is electromagnetic radiation with wavelengths longer than visible red light, but shorter than microwaves.**

The electromagnetic spectrum is roughly:

```text
short wavelength                                      long wavelength
    │                                                      │
    ▼                                                      ▼
   γ-rays → X-rays → UV → visible → infrared → microwave → radio
                              │
                         red → IR
```

Typical infrared wavelengths:

$$
\boxed{700\text{ nm} \sim 1\text{ mm}}
$$

More precisely, the boundary with visible light is conventionally around **700–750 nm**, and the boundary with microwaves is around **1 mm**.

### The important physics

Like visible light, infrared is made of **photons**. A photon's energy is

$$
E = h\nu = \frac{hc}{\lambda}
$$

So longer wavelength means lower photon energy.

For example:

* visible red: \\(\lambda \approx 650\text{ nm}\\)
* near-IR: \\(\lambda \approx 850\text{ nm}\\)
* thermal IR: \\(\lambda \approx 10\ \mu m\\)

An IR photon therefore has less energy than a visible-light photon.

### Why do we associate IR with heat?

Because ordinary objects at room temperature emit a lot of electromagnetic radiation in the infrared.

For a blackbody, the peak wavelength approximately follows Wien's law:

$$
\lambda_{\max} = \frac{b}{T}
$$

For room temperature, \\(T\approx300K\\):

$$
\lambda_{\max}
\approx
\frac{2.9\times10^{-3}}{300}
\approx 9.7\ \mu m
$$

That's **infrared**.

So when you feel heat from:

```text
your hand
   ↓
infrared photons
   ↓
your skin
```

you're literally receiving electromagnetic radiation emitted by the warmer object.

This is also why a **thermal camera** can "see" people in darkness: it isn't seeing visible photons; it's detecting infrared radiation associated with the objects' temperatures.

### IR isn't one single thing

It's useful to split it into:

```text
Near IR       ~0.7–1.4 μm
Short-wave IR ~1.4–3 μm
Mid-wave IR   ~3–8 μm
Long-wave IR  ~8–15 μm
Far IR        ~15 μm–1 mm
```

Different wavelengths interact with matter differently.

For example:

* **850/940 nm IR LEDs** → remote controls, sensors, cameras
* **~1.3/1.55 μm** → optical fiber communications
* **~3–5 μm** → many thermal/industrial sensing applications
* **~8–14 μm** → thermal imaging, because Earth's atmosphere has a useful transmission window there

The key idea is:

> **Infrared isn't "a type of heat." It's electromagnetic radiation. Heat is energy transferred between systems; IR is one mechanism by which that energy can be transferred.**

And mathematically, **IR is just light with a longer wavelength / lower frequency than visible red light.**

References:

* [NASA — Infrared Waves](https://science.nasa.gov/ems/07_infraredwaves/)
* [Encyclopaedia Britannica — Infrared radiation](https://www.britannica.com/science/infrared-radiation)
* [NIST — Electromagnetic Spectrum](https://www.nist.gov/pml/owm/metric-si/si-units-quantities)
