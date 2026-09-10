---
audio: false
generated: true
image: false
lang: en
layout: post
title: Invisible Autofocal Eyeglasses
translated: false
type: note
---

Question: **How could you build eyeglasses that are almost invisible/clear and dynamically change optical power based on what you're looking at?**

Answer: **Yes. This is technically feasible, and the architecture is surprisingly clean.** What you are describing is essentially an **autofocal / adaptive-focus prescription lens**: the lens continuously changes its dioptric power based on gaze direction + target distance.

Your “just barely clear” idea makes this particularly interesting: instead of a fixed `-5.00 D` lens, the glasses could dynamically choose something like `-3.50 D`, `-4.20 D`, `-4.80 D`, etc., depending on the distance you are actually looking at. Your page explicitly describes scenario-dependent prescription rather than one fixed prescription. ([Zhiwei Li][1])

### 1. The basic system

```text
                    ┌──────────────────┐
                    │  Eye tracking    │
                    │  cameras / IR    │
                    └────────┬─────────┘
                             │ gaze vector
                             ▼
                    ┌──────────────────┐
                    │ Target distance  │
                    │ estimation       │
                    └────────┬─────────┘
                             │ depth
                             ▼
                    ┌──────────────────┐
                    │ Focus controller │
                    │                  │
                    │ target D = f(z)  │
                    └────────┬─────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │ Electrically tunable lens  │
              │                            │
              │  - liquid lens             │
              │  - LC lens                 │
              │  - Alvarez lens             │
              └─────────────┬──────────────┘
                            │
                            ▼
                         YOUR EYE
```

This has already been demonstrated experimentally. The Stanford/Meta-style **Autofocals** research combined binocular eye tracking, a depth camera and electronically controlled liquid lenses to automatically adjust focal power. ([PubMed][2])

One prototype achieved roughly **4.3 D of dynamic accommodation**, ~67 ms control calculations, and about 19 hours of operation. ([PubMed][3])

---

## 2. The really important part: the lens

You don't want an LCD display.

You want a **transparent optical element whose refractive power can change**.

There are several approaches.

### A. Liquid lens — probably the best DIY starting point

Imagine:

```text
       transparent membrane
          _________
       /           \
      /   liquid    \
     |               |
      \             /
       \___________/

          curvature R
              ↓
         focal power D
```

Change the pressure/volume of liquid → change membrane curvature → change focal length.

The approximate relationship is:

$$
P = \frac{1}{f}
$$

where:

* `P` = optical power in diopters
* `f` = focal length in meters

So:

```text
f = 1.0 m  →  +1.0 D
f = 0.5 m  →  +2.0 D
f = 0.25 m →  +4.0 D
```

A published adaptive-eyeglasses design uses a fluid-filled variable-focus lens with a thin membrane and microfluidic actuator. It demonstrated about **3 D** of variable power. ([PubMed][4])

There is even a recent Georgia Tech prototype using a PDMS/silicone-oil membrane whose curvature changes with injected fluid volume. ([Georgia Tech Repository][5])

For a garage prototype, I'd start here.

---

## 3. But you need to solve your astigmatism separately

This is the subtle part.

A spherical variable lens only gives you:

$$
S
$$

But a prescription is:

$$
S + C \times \theta
$$

where:

* `S` = spherical power
* `C` = cylinder
* `θ` = cylinder axis

Your own historical prescriptions contain substantial astigmatism, so a practical device cannot simply make the whole lens `-3 D → -5 D`.

You need something like:

```text
                   spherical
                       +
               ┌─────────────┐
               │ variable S  │
               └─────────────┘
                       +
               ┌─────────────┐
               │ fixed C/axis│
               └─────────────┘
```

A very practical first prototype therefore uses:

**fixed astigmatism correction + variable spherical correction.**

That's dramatically easier.

---

# 4. "Based on what I see" needs two sensors

You don't actually need computer vision to understand the whole scene.

You mainly need:

### Eye gaze

```text
IR LED → eye
          ↓
      IR camera
          ↓
     pupil position
          ↓
     gaze direction
```

### Target depth

For example:

```text
             object
               ●
              / \
             /   \
            /     \
         camera    camera

             stereo
               ↓
          depth estimate
```

Or use a tiny ToF sensor.

Then:

$$
d = \text{distance to object}
$$

and the controller calculates:

$$
D_{\text{target}} \approx \frac{1}{d}
$$

for the accommodation component.

The original Autofocals system used exactly the important combination: **binocular eye tracking + depth sensing**, because gaze error alone can produce noticeable focus errors. ([PubMed Central (PMC)][6])

---

# 5. You can make the control loop extremely simple

Suppose your base prescription is:

```text
L: -3.00 D
R: -5.00 D
```

You look at:

```text
∞      → correction = base prescription
2 m    → small adjustment
1 m    → stronger near adjustment
50 cm  → stronger near adjustment
30 cm  → strongest near adjustment
```

Controller:

```python
def desired_power(distance_m):
    accommodation = 1.0 / distance_m

    # personal calibration
    accommodation = clamp(accommodation, 0, MAX_ADD)

    return base_power + accommodation
```

Then don't immediately jump:

```python
lens.set_power(target)
```

because that would feel terrible.

Use a low-pass / slew-rate controller:

```python
power += clamp(
    target_power - power,
    -MAX_STEP,
    MAX_STEP,
)
```

You basically want:

```text
eye movement
    ↓
gaze estimate
    ↓
depth estimate
    ↓
target optical power
    ↓
smooth transition
    ↓
tunable lens
```

---

# 6. The coolest version: gaze-contingent "just barely clear"

This is where your idea gets more interesting than ordinary autofocus glasses.

Instead of:

```text
distance → mathematically calculated prescription
```

you could implement:

```text
distance
   ↓
initial estimate
   ↓
small optical adjustment
   ↓
visual feedback
   ↓
"clearer / worse?"
   ↓
gradient search
   ↓
optimal power
```

Essentially:

$$
D_{t+1}=D_t-\eta \frac{\partial L}{\partial D}
$$

where `L` is some measure of visual blur/discomfort.

But **the eye itself is not an easy camera sensor**, so I wouldn't try to infer blur directly from retinal imagery in version 1.

Instead:

```text
depth sensor
      +
eye tracking
      +
personal calibration
      ↓
predicted optimal D
```

is much easier.

Then later experiment with biological feedback.

---

# 7. What I'd actually build

Given your hardware/repair/EE direction, I would **not start by trying to manufacture a beautiful pair of glasses**.

Build a bench prototype:

```text
                 ESP32 / STM32
                      │
          ┌───────────┴───────────┐
          │                       │
       ToF sensor              motor
          │                       │
          │                 ┌─────▼─────┐
          │                 │ variable  │
          │                 │ liquid    │
          │                 │ lens      │
          │                 └───────────┘
          │
          ▼
       distance
```

Start with **one eye**.

For example:

```text
fixed -4.00 D lens
        +
variable +0 → +3 D lens
```

Now put objects at:

```text
∞
2 m
1 m
70 cm
50 cm
33 cm
25 cm
```

and measure whether you can maintain sharp vision.

Once that works:

```text
                    ┌── eye camera
                    │
                    ├── ToF
                    │
MCU ────────────────┼── tunable lens
                    │
                    └── encoder / pressure sensor
```

Then make it binocular.

---

## 8. If your requirement is literally "barely visible"

There are two different meanings of *barely clear*.

### Optical transparency

You want:

```text
lens transmission ≈ high
no display
no projection
no opaque electronics in optical path
```

Liquid lenses are attractive because the active optical region can remain transparent.

### Minimal physical visibility

Put everything into the frame:

```text
       ┌───────────────────────────┐
       │ IR camera       IR camera │
       │      \           /        │
       │       \         /         │
       │        [ lenses ]         │
       │                           │
       │  MCU   battery   ToF      │
       └───────────────────────────┘
```

The optical aperture itself stays basically like ordinary glasses.

---

## 9. Alternative: Alvarez lens

Another fascinating option is an **Alvarez lens**.

Two specially shaped lenses slide laterally:

```text
        lens A
      ╭────────╮
       ╲╱╲╱╲╱

          ⇆

       ╱╲╱╲╱╲
      ╰────────╯
        lens B
```

Changing their relative position changes optical power.

Advantages:

* no liquid
* mechanically understandable
* potentially very high optical quality
* easy to control with a tiny motor

Disadvantages:

* moving optics
* thicker
* harder to make cosmetically invisible

Alvarez-type approaches are one of the established variable-focus approaches alongside liquid and LC lenses. ([DOI][7])

---

## 10. Liquid crystal is even more futuristic

An electrically driven LC lens can change refractive index:

$$
n = n(V)
$$

so:

$$
f = f(V)
$$

No moving mechanical parts.

Recent research has demonstrated tunable LC lenses with roughly **0–2.5 D** continuous focus tuning, response around **0.5 s**, and low-voltage operation. ([DOI][8])

But LC has nasty optical engineering problems: polarization, limited phase shift, diffraction orders, contrast and aberrations. ([DOI][7])

So for **your first hardware experiment**, I'd choose:

> **fixed astigmatism lens + liquid variable spherical lens + ToF + IR eye tracking + MCU**

rather than LC.

That is a very real engineering project, not sci-fi. The key research precedent already exists; the interesting part for you would be making it **lighter, cheaper, transparent, and optimized around your "just barely clear" control strategy**. ([PubMed][2])

References:

* [Your vision notes](https://lzwjava.com/vision-tips-en?utm_source=chatgpt.com)
* [Autofocals: Evaluating gaze-contingent eyeglasses](https://pubmed.ncbi.nlm.nih.gov/31259239/?utm_source=chatgpt.com)
* [Correcting Presbyopia With Autofocusing Liquid-Lens Eyeglasses](https://pubmed.ncbi.nlm.nih.gov/34232861/?utm_source=chatgpt.com)
* [Adaptive eyeglasses for presbyopia correction](https://pubmed.ncbi.nlm.nih.gov/31052911/?utm_source=chatgpt.com) 

I can also turn this into a **$100–300 bench prototype BOM + circuit/block diagram + control firmware architecture** using parts you could realistically source and experiment with.

[1]: https://lzwjava.com/vision-tips-en "Comfortable Daily Eyeglass Use at 1.50D Below Full Prescription"
[2]: https://pubmed.ncbi.nlm.nih.gov/31259239/?utm_source=chatgpt.com "Autofocals: Evaluating gaze-contingent eyeglasses for presbyopes - PubMed"
[3]: https://pubmed.ncbi.nlm.nih.gov/34232861/?utm_source=chatgpt.com "Correcting Presbyopia With Autofocusing Liquid-Lens Eyeglasses."
[4]: https://pubmed.ncbi.nlm.nih.gov/31052911/?utm_source=chatgpt.com "Adaptive eyeglasses for presbyopia correction: an original variable-focus technology - PubMed"
[5]: https://repository.gatech.edu/entities/publication/69bdcd80-f316-4b11-ace9-e6c78b25f20c?utm_source=chatgpt.com "Design and Evaluation of Liquid-Based Tunable-Lens Eyeglasses for Automatic Focus Adjustment"
[6]: https://pmc.ncbi.nlm.nih.gov/articles/PMC6598771/?utm_source=chatgpt.com "Autofocals: Evaluating gaze-contingent eyeglasses for presbyopes - PMC"
[7]: https://doi.org/10.1364%2FOE.27.010533?utm_source=chatgpt.com "Adaptive eyeglasses for presbyopia correction: an original variable-focus technology"
[8]: https://doi.org/10.1364/BOE.557747?utm_source=chatgpt.com "Dynamic presbyopia correction in the macular field of view by using a liquid crystal lens"
