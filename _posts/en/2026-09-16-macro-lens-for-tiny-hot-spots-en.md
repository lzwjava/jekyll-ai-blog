---
audio: false
generated: true
image: false
lang: en
layout: post
title: Macro Lens for Tiny Hot Spots
translated: false
type: note
---

Question: **Why do you need the macro lens on the FR03D?**

Answer: **Because thermal cameras have limited spatial resolution, and PCBs contain tiny objects.** The macro lens lets the camera get physically closer and resolve those tiny hot spots.

Think of it like this:

```text
Without macro lens

Camera
  ↓
 [ PCB ]
 ┌──────────────────────────────┐
 │  ▪ IC    ▪ C    ▪ R    ▪     │
 │                              │
 └──────────────────────────────┘

Camera sees:
      █████████████
      █████████████
      █████████████
```

At normal working distance, one thermal pixel might correspond to several millimeters of PCB. A tiny 1 mm capacitor that is overheating can get **averaged together with the surrounding PCB**.

With macro:

```text
Camera
  ↓
  🔍
 ┌─────────────┐
 │  C  C  R    │
 │  ▓▓▓▓▓      │ ← localized heat
 │  IC         │
 └─────────────┘
```

Now you can distinguish:

```text
PCB:       38°C
Cap:       41°C
IC:        43°C
MOSFET:    91°C  ← obvious
```

rather than seeing one blurry ~50°C region.

### The important distinction

A macro lens **doesn't increase the thermal sensor's native resolution**.

If the FR03D sensor is 240×240:

```text
sensor = 240 × 240 pixels
```

stays exactly that.

The macro lens changes the **field of view / magnification**, so those 240×240 pixels cover a much smaller physical area:

```text
normal lens:

240 pixels → ~100 mm PCB width

macro lens:

240 pixels → ~20 mm PCB width
```

So you sacrifice coverage to gain **spatial detail**.

### For your use case

If you're doing:

**PC motherboard / GPU / PSU / large PCB**

→ macro is useful but not absolutely necessary.

**Phone / laptop motherboard / small SMD components**

→ **I'd definitely get the macro lens.**

**Finding which tiny component is causing a short**

→ **macro lens is particularly valuable.**

The killer workflow is:

```text
1. Power board
2. Inject current
3. Scan entire board
4. Find hot region
5. Put macro lens on
6. Move very close
7. Identify the actual component
```

So I'd consider the macro lens **not an accessory for "better temperature accuracy"; it's an accessory for better spatial resolution on tiny objects.**
