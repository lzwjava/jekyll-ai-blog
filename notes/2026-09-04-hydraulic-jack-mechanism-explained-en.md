---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hydraulic Jack Mechanism Explained
translated: false
type: note
---

Question: How does a hydraulic jack actually work?

Answer: A hydraulic jack is basically **a pressure multiplier + one-way valves + a hydraulic cylinder**.

![Image](https://images.openai.com/static-rsc-4/geLvdQMwvpgfZ3yv33Tgqy3qRVTwnvfoDOsiCxcXQo_GXuJDlCJi-hL5uwbwzPzh_RNVeK-sIOH396vDTUYUG9uoXxPR_9D72_vva4HSvmb6pp2JqQPZc_JUkZe_49TvuL-BkYy29wnYPLByrB8tm2EYx9lAX6gIx0ZI73ZZUppVIWzofgTKDaRYpaJIsMG8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AQHHBtTiQXSyOtFxJPsFUhM_ckxDEMhMcl7FAUrQKYvtx1GqkcH3k6DjkkCjUOoddRv2PMMoBJ2t1cVsCsFEhIlRdKZKvMNA3ZXgJIyL_RBvem4odX2Fm8BeQecsRVNAYTiSMOUqxWoW3HkgOv0OkL2UFhY05KxIFriAeOxxr9dUIiZ8ZwH85O2AG10_NuxL?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/v0nUVbthREMOLwwQIbGpPCFaRjPT1C5nzUSOldfqoteBptZur8oEVom8O2iQ8mZhNy2-ELcpoTplaTFY1kkjdAC3YokbF-1VZba5hih7h7smJadEDpzJhGvntSm_MSP7sgLQR166Y_4_V2uU_KfX6maCVjvsHY3jjmaJhHUf4jgXWwNGv2H2hxLu50sJJtXv?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/zQr9LaMk4akxDXtIGUTHmyADMgCX4PMcEjpUWGehoKHSC0OgQ5FYAm9IvlAV9hRvrmTrcGpSg_mse69qLFzTzhXyZ9ej1kdZ6Vg2ZiDN_9DNH5Lap20e2we0swMxZnbUOZsMBogPJcDsdqVGPpxZ5j675ZARNrh3AxyLyBhk-zAjfOKogLzQefOqDNBjcRLZ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/m3w28bfozHQ29Zmso2LxPIlImSndabR_Haych7ARc7mYbH6QHG4--4K6ssKgqEP_ow6kLadKfRDTjofwC7OPXFVejlZ06vJDCMGuthUrgJ5XqFqbyFNVgjO4Fv7PoPeMA2ICA1lJSyv1oEYS5xLRMw7mAIvq8NNHGctabJj2-9BfOQ-dnpjnR9BiLSRNwNwk?purpose=fullsize)

### 1. The key idea: Pascal's law

If you push hydraulic oil with a small piston:

$$
P=\frac{F_1}{A_1}
$$

That pressure is transmitted through the oil:

$$
P=\frac{F_2}{A_2}
$$

Therefore:

$$
\boxed{F_2=F_1\frac{A_2}{A_1}}
$$

For example:

* Small pump piston: \\(A_1=1\,cm^2\\)
* Large lifting piston: \\(A_2=20\,cm^2\\)
* You push with \\(F_1=100N\\)

Then:

$$
F_2=100\times20=2000N
$$

So a relatively small hand force can produce a large lifting force.

---

### 2. What happens when you pump the handle?

Inside the jack there are essentially **two pistons and check valves**:

```text
             CAR
              ↓
        ┌────────────┐
        │ LIFT PISTON│  ← large piston
        └─────┬──────┘
              │
       ┌──────┴───────┐
       │  HIGH PRESS. │
       │     OIL      │
       └───┬──────┬───┘
           ↑      │
      check valve │
           ↑      ↓
       ┌────────────┐
       │ PUMP       │ ← small piston
       └─────┬──────┘
             │
          OIL TANK
```

When you move the handle:

**Stroke 1 — pump piston retracts**

Oil is sucked from the reservoir into the pump chamber.

**Stroke 2 — pump piston pushes**

The inlet check valve closes.

The outlet check valve opens.

Oil is forced into the high-pressure cylinder.

**Stroke 3 — lift piston moves**

More oil enters the large cylinder → the large piston moves upward.

Repeat this hundreds of times and the car rises.

---

### 3. Why doesn't the car fall immediately?

Because of the **check valve**.

Think of it as:

```text
Oil →  YES
     ───────>

Oil ←  NO
     ✕
```

Each pump stroke adds a little more oil to the high-pressure side.

The valve prevents that oil from flowing backward into the reservoir.

---

### 4. Then what does the release valve do?

This is the important part related to what you just did.

Normally:

```text
RESERVOIR
    │
    │   ✕ closed
    │
    └────── HIGH-PRESSURE CYLINDER
```

When you turn the **release valve**, you create a path:

```text
HIGH-PRESSURE CYLINDER
          │
          ↓
       RELEASE
        VALVE
          │
          ↓
      RESERVOIR
```

The oil flows back into the reservoir.

The lifting piston goes down.

That's why the jack lowers.

So the release valve is basically a **controlled hydraulic bypass**.

---

### 5. And this explains your oil spill

You removed the valve/plug completely.

That's different from simply **opening the release valve a little**.

You effectively opened a hole in the hydraulic system:

```text
HIGH PRESSURE / OIL CIRCUIT
          │
          ↓
      [ OPEN HOLE ]
          │
          ↓
      🛢️ OIL SPILLS
```

Depending on exactly which part you removed, you may have opened the reservoir or another section of the hydraulic circuit.

That's why you suddenly got the **messy oil spill**.

---

### 6. The beautiful part

A hydraulic jack doesn't create energy from nowhere.

You trade:

**small force + large distance**

for

**large force + small distance**

Approximately:

$$
F_1d_1 \approx F_2d_2
$$

So if the lifting piston has 20× the area, you can get roughly 20× the force, but the small pump piston has to move roughly 20× farther.

That's why you can lift a ~2-ton car with a relatively small handle force.

**The jack is essentially a mechanical lever driving a tiny hydraulic pump, which repeatedly injects oil into a much larger cylinder.**
