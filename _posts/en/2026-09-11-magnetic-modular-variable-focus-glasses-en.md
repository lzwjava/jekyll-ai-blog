---
audio: false
generated: true
image: false
lang: en
layout: post
title: Magnetic modular variable focus glasses
translated: false
type: note
---

Question: **You mean the magnetic clip-on glasses are mainly a lightweight modular design, not glasses whose optical power dynamically changes.**

Answer: **Exactly. They're two very different ideas.**

Typical magnetic clip-ons are basically:

```text
normal prescription glasses
        +
magnetic auxiliary lens
        ↓
different optical function
```

For example, you can snap on sunglasses, reading lenses, filters, etc. Some systems explicitly offer magnetic reader clips from **+0.50 to +2.50 D**. ([Chemistrie][1])

But the lens itself is **static**. You physically add/remove it.

What you're describing is:

```text
             ┌─────────────────┐
             │ normal glasses  │
             └────────┬────────┘
                      │
                electrically
                  controlled
                      │
                      ▼
             ┌─────────────────┐
             │ variable-focus  │
             │ optical element │
             └─────────────────┘
                      │
                      ▼
                  your eye
```

So instead of:

```text
OFF → -4 D
ON  → -2 D
```

you want:

```text
      continuously variable

-4.00 ─ -3.75 ─ -3.50 ─ -3.25 ─ ... ─ -1.00 D
```

### And magnetic mounting could actually be useful

This is where your idea gets interesting.

You could make the **adaptive optical module itself removable**:

```text
             ordinary frame
          ┌──────────────────┐
          │                  │
          │    [ MAGNET ]    │
          │      ↓           │
          │   ┌────────┐     │
          │   │ VFL    │     │
          │   │ module │     │
          │   └────────┘     │
          │      ↑           │
          │    MAGNET        │
          └──────────────────┘
```

The base glasses could remain extremely light:

```text
Base:
    frame
    fixed prescription
    battery
    controller

Magnetic module:
    tunable lens
    eye tracking
    ToF/depth sensor
```

Then you could literally **snap the smart optical layer onto ordinary glasses**.

That's much more realistic than trying to put every component into a conventional eyeglass lens from day one.

And the underlying variable-focus technology already exists. A 2019 adaptive-eyeglasses prototype used a fluid-filled lens with an ultrathin deformable membrane and automatic distance sensing, achieving about **3 D of variable optical power**. ([PubMed][2])

Another prototype demonstrated a **32-mm aperture, 5.6-D range, <20 mW electrical consumption**, although the complete tunable lens was still 8.4 mm thick and 14.4 g. ([PubMed Central (PMC)][3])

So I would separate the problem into:

**1. Magnetic clip-on = mechanical modularity/lightness**

**2. Variable-focus lens = adaptive optical power**

**3. Eye/depth sensing = deciding the required power**

**4. Controller = continuously driving the lens**

The really cool product would combine **all four**:

> **a normal-looking ~10–20 g pair of glasses where the optical prescription is software-controlled, and the adaptive module can be magnetically removed.**

That is much closer to an actual engineering/product direction than "AI glasses" with a display.

[1]: https://chemistrie.com/products/clip-on-reader-lenses?utm_source=chatgpt.com "Reader Clips - Magnetic Reading Lenses | Chemistrie"
[2]: https://pubmed.ncbi.nlm.nih.gov/31052911/?utm_source=chatgpt.com "Adaptive eyeglasses for presbyopia correction: an original variable-focus technology - PubMed"
[3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5772464/?utm_source=chatgpt.com "Tunable-focus lens for adaptive eyeglasses - PMC"
