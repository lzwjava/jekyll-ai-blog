---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Silicon Wafer and Chip Fabrication
translated: false
type: note
---

**Question:** What is a wafer in chip manufacturing?

**Answer:**

A wafer is the thin, circular slice of ultra-pure monocrystalline silicon that serves as the substrate on which integrated circuits are fabricated. It's the "canvas" — every chip (die) you've ever used, from your M2's cores to the MI300X's compute dies, started life as a region on a wafer.

**From sand to wafer (first principles):**

1. **Purification** — Quartz sand (SiO₂) is reduced to metallurgical-grade silicon, then refined via the Siemens process to electronic-grade silicon: 99.9999999% pure ("9N"). Impurity levels matter because a single stray atom per ~billion changes carrier concentration, and transistor behavior depends entirely on *controlled* doping.

2. **Crystal growth (Czochralski process)** — Polysilicon is melted at ~1,414°C in a quartz crucible. A small seed crystal is dipped in and slowly pulled upward while rotating. Atoms freeze onto the seed following its lattice orientation, growing a single-crystal cylindrical ingot (boule) up to ~2m long. Single-crystal matters: grain boundaries in polycrystalline silicon scatter carriers and kill transistor performance.

3. **Slicing** — The ingot is sawed with diamond wire into wafers ~775 µm thick (for 300mm wafers), then ground, lapped, etched, and polished to atomic-level flatness. Surface roughness must be sub-nanometer because you're about to pattern features a few nm wide on it.

**Sizes:** Industry-standard is 300mm (12-inch) diameter today; older fabs run 200mm. The push to 450mm stalled because of cost. Bigger wafers = more dies per wafer = lower cost per die, since most processing steps (lithography exposure aside) cost roughly the same per wafer regardless of die count.

**How chips come off it:** Hundreds of fabrication steps — deposition, lithography, etch, ion implantation, CMP — build transistors and ~15+ metal interconnect layers across the entire wafer simultaneously. A stepper/EUV scanner exposes one reticle field (~26×33mm max) at a time, stepping across the wafer. Afterward, dies are tested (wafer probe), the wafer is diced, and good dies are packaged.

**The economics you'll care about as someone watching GPU supply:**

```python
import math

def dies_per_wafer(die_w_mm, die_h_mm, wafer_d_mm=300, scribe=0.1):
    # Standard approximation accounting for edge loss
    die_area = (die_w_mm + scribe) * (die_h_mm + scribe)
    r = wafer_d_mm / 2
    return int(math.pi * r**2 / die_area - math.pi * wafer_d_mm / math.sqrt(2 * die_area))

def yield_rate(die_area_cm2, defect_density=0.1):
    # Murphy/Poisson model: D0 in defects per cm^2
    return math.exp(-defect_density * die_area_cm2)

# H100-class die: ~814 mm^2 (near reticle limit)
w, h = 26.0, 31.3
n = dies_per_wafer(w, h)
y = yield_rate(w * h / 100, defect_density=0.1)
print(f"dies/wafer: {n}, yield: {y:.1%}, good dies: {int(n*y)}")
# dies/wafer: ~60, yield: ~44%, good dies: ~26
```

This is why huge monolithic dies are brutally expensive — yield decays exponentially with area — and why your MI300X is a chiplet design: AMD fabricates 8 smaller XCD compute dies (TSMC N5) plus IO dies (N6) and stitches them with 3D packaging. Small dies → high yield per die → bin out the bad ones instead of throwing away an 800mm² monster.

One defect density number (D0) basically determines whether a node is economically viable, which is why "TSMC N3 yield" headlines move markets.
