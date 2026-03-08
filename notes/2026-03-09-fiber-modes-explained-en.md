---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fiber Modes Explained Simply
translated: false
type: note
---

Question: What do multimode fiber and single mode mean in fiber optics?

Answer:

## Fiber Optic Basics

A fiber optic cable transmits data as pulses of light through a glass or plastic strand. The **"mode"** refers to the path (or ray) that light takes as it travels through the fiber core. How many modes of light can travel simultaneously is the core distinction between these two types.

---

## Single Mode Fiber (SMF)

Single mode means the fiber enables **one type of light mode** to be propagated at a time.

**Key characteristics:**

- Single mode has a core diameter of **8–9 µm** and uses a **laser** to carry one light mode over long distances with low loss.
- In single mode fiber, modal and light dispersion is negligible, so the light wave transmits in a linear manner. This reduces attenuation and keeps signal strength consistent over long distances.
- Standard wavelengths are **1310 nm and 1550 nm**, which provide low attenuation for long-distance transmission.
- Single mode is used to send signals at great distances — up to **100 km** before the signal needs re-amplification, making it ideal for WAN applications.
- Single mode cables are typically **color-coded yellow.**
- Classified into **OS1** and **OS2** types.

---

## Multimode Fiber (MMF)

Multimode means the fiber can **propagate multiple modes** simultaneously.

**Key characteristics:**

- Multimode fiber has a larger core ranging from **50 to 100 microns** in diameter. This larger core permits multiple light modes to travel simultaneously, but makes it susceptible to signal attenuation over shorter distances.
- Multimode fiber uses **LEDs or VCSELs** as the light source and operates at standard wavelengths of **850 nm and 1300 nm.**
- Multimode fiber sees the most use in **LAN environments** where large amounts of bandwidth need to be moved over many short distances — such as in NAS or database applications.
- Multimode cables are typically **color-coded orange or aqua.**
- Graded from **OM1 to OM5**, with OM1 being the oldest (62.5 µm) and OM3/OM4/OM5 being 50 µm with higher performance.

---

## Key Comparison Table

| Feature | Single Mode (SMF) | Multimode (MMF) |
|---|---|---|
| Core Diameter | ~9 µm | 50 or 62.5 µm |
| Light Source | Laser | LED / VCSEL |
| Wavelength | 1310 nm, 1550 nm | 850 nm, 1300 nm |
| Max Distance | Up to ~100 km | Up to ~550 m (OM4) |
| Bandwidth | Virtually unlimited | Limited by modal dispersion |
| Cost | Higher (expensive transceivers) | Lower (cheaper transceivers) |
| Jacket Color | Yellow | Orange or Aqua |
| Use Case | WAN, long-haul, telecom | LAN, data centers, buildings |

---

## Why Can't You Mix Them?

Multimode fiber and single mode fiber have different core sizes and transmit different numbers of light modes. If you mix the two or connect them directly, you'll lose a large amount of signal (optical loss), resulting in a link flapping or going down.

---

## Which Should You Choose?

- Multimode optical fiber easily supports most distances required for enterprise and data center networks at a cost significantly less than single mode — making it the more cost-effective choice for shorter-reach applications up to the 500–600 meter range.
- Beyond that range, single mode optical fiber becomes necessary.

References:

- [https://www.fs.com/blog/fiber-optic-cable-types-single-mode-vs-multimode-fiber-cable-1310.html](https://www.fs.com/blog/fiber-optic-cable-types-single-mode-vs-multimode-fiber-cable-1310.html)
- [https://www.ofsoptics.com/single-vs-multimode-fiber/](https://www.ofsoptics.com/single-vs-multimode-fiber/)
- [https://jonard.com/blog/singlemode-fiber-vs-multimode-fiber-what-difference](https://jonard.com/blog/singlemode-fiber-vs-multimode-fiber-what-difference)
- [https://patchbox.com/blog/single-mode-vs-multimode-fiber-difference/](https://patchbox.com/blog/single-mode-vs-multimode-fiber-difference/)
- [https://www.gomultilink.com/blog/multilog/single-mode-vs-multi-mode-fiber-optic-cables](https://www.gomultilink.com/blog/multilog/single-mode-vs-multi-mode-fiber-optic-cables)