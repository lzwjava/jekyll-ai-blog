---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1310 nm Wavelength Not Speed
translated: false
type: note
---

Question: How should I understand a WAN interface specified as **1310 nm**?

Answer:

If you see something like:

```text
WAN interface
  wavelength: 1310 nm
```

the **1310 nm is the optical wavelength of the fiber signal**, not the interface speed.

Think of a fiber link as:

```text
Router/Switch
    │
    │ electrical
    ▼
┌──────────┐
│   SFP    │  ← laser/transceiver
└────┬─────┘
     │
     │ 1310 nm optical light
     ▼
══════════════════════════════ fiber
     │
     ▼
┌──────────┐
│   SFP    │
└────┬─────┘
     │
     ▼
Router/Switch
```

### Why 1310 nm?

Fiber communication uses particular wavelength "windows" where optical fiber has favorable loss characteristics.

Typical Ethernet optics:

| Wavelength  | Typical use              |  Rough reach |
| ----------- | ------------------------ | -----------: |
| **850 nm**  | Multimode, SR            |   ~100–300 m |
| **1310 nm** | Single-mode, LR/ER       |    ~10–40 km |
| **1550 nm** | Long-haul / DWDM / ER/ZR | tens–100+ km |

The important thing is that **1310 nm is an optical carrier**, while the data is encoded by rapidly modulating that light.

For example, a `10GBASE-LR` transceiver typically looks conceptually like:

```text
laser
  ↓
1310 nm light
  ↓
modulated billions of times/sec
  ↓
10 Gb/s data
```

So:

```text
1310 nm ≠ 1310 Mbps
1310 nm ≠ 1310 MHz
1310 nm ≠ "WAN speed"
```

It's simply the **color/frequency of the infrared light**.

The corresponding frequency is:

$$
f = \frac{c}{\lambda}
$$

For λ = 1310 nm:

$$
f \approx \frac{3\times10^8}{1.31\times10^{-6}}
\approx 229\text{ THz}
$$

So you're sending a ~229 THz optical carrier and modulating it to carry the digital signal.

### What matters when connecting two WAN interfaces

Suppose you have:

```text
Router A                    Router B
1310 nm SFP  ────────────── 1310 nm SFP
       SMF fiber
```

You generally need to match more than just wavelength:

```text
                 A                 B
wavelength       1310 nm     ↔    1310 nm
fiber            SMF         ↔    SMF
speed             10G        ↔     10G
standard       10GBASE-LR   ↔  10GBASE-LR
connector          LC        ↔      LC
```

For **BiDi** optics, there's an extra wrinkle:

```text
A: TX 1270 nm / RX 1330 nm
B: TX 1330 nm / RX 1270 nm
```

Here you intentionally use different wavelengths in each direction over **one fiber**.

So if you're looking at a real WAN interface specification that says something like **"1310 nm"**, paste the **full interface/SFP specification**. The interesting part is usually figuring out whether it is **1310 nm LR, BiDi, CWDM, PON, etc.**, because that determines what fiber/transceiver you can actually connect.
