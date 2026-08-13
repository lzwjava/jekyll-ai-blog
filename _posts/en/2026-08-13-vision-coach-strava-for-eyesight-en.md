---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Vision Coach: Strava for Eyesight"
translated: false
type: note
---

Question: **What app/product could we build from the ideas in your Vision Tips page?**

Answer:

I think there is a much better product here than simply building a **“myopia reversal app.”**

Your page already contains the seed of a product: **turn vision correction into a measurable, adaptive, personal experiment.** The interesting part is not the claim that `-1.50D` is universally optimal; it is the combination of:

* prescription
* viewing distance
* screen usage
* “barely clear” threshold
* glasses used in different contexts
* longitudinal measurements
* experimentation
* personal feedback

Your page explicitly describes this as a 3-year hands-on experiment, with prescription measurements over time. ([Zhiwei Li][1])

### 1. My favorite: **Vision Coach**

Think:

> **Strava for eyesight.**

Not a medical diagnosis app. A personal vision-training / measurement / experiment tracker.

The core loop:

```text
                    ┌──────────────┐
                    │  Your eyes   │
                    └──────┬───────┘
                           │
                    phone camera
                           │
                           ▼
                ┌──────────────────┐
                │ Vision Coach     │
                │                  │
                │ distance         │
                │ text clarity     │
                │ screen time      │
                │ glasses          │
                │ symptoms         │
                └────────┬─────────┘
                         │
                         ▼
                 personal model
                         │
             ┌───────────┴──────────┐
             ▼                      ▼
       daily guidance          progress graph
```

Every day it could ask:

> **What are you doing?**

* Computer
* Phone
* Reading
* Walking
* Driving
* Watching TV
* Outdoors

Then:

> **What glasses are you wearing?**

And:

> **How far is the screen?**

The phone can estimate distance using the camera / AR depth where available.

Then the app records:

```json
{
  "activity": "computer",
  "distance_cm": 65,
  "glasses_delta_d": -1.50,
  "duration_min": 142,
  "clarity": 0.8,
  "strain": 0,
  "date": "2026-08-13"
}
```

Now you have something much more interesting than a blog.

---

### 2. The killer feature: **automatic “barely clear” measurement**

This is where AI/vision makes the product interesting.

Instead of:

> “Wear -1.50D glasses.”

the app could continuously estimate:

```text
Your current working distance: 63 cm

Estimated focal demand:
    1 / 0.63 ≈ 1.59 D

Current prescription:
    -4.25 D

Current near correction:
    -2.75 D

Status:
    🟢 barely clear
```

The `1 / distance(m)` relationship is already part of your page. ([Zhiwei Li][1])

Even better, periodically run a controlled test:

```text
Look at this text.

Move the phone until it becomes barely unclear.

        ←────── 62 cm ──────→

Your threshold:
        62 cm

Previous:
        58 cm

Change:
        +4 cm
```

That gives the user **an actual measurement**, rather than just “I feel my eyes are better.”

---

### 3. A very cool product: **Vision Meter**

Actually, I'd MVP this first.

Open app:

```text
┌─────────────────────────┐
│                         │
│        20 / 20          │
│                         │
│      E F P T O Z        │
│                         │
│      F P T O L P        │
│                         │
│      T O Z L P E        │
│                         │
│                         │
│      57.4 cm            │
│                         │
│  Move until barely clear│
└─────────────────────────┘
```

The phone knows:

* screen dimensions
* viewing distance
* font size
* text size
* user's response

You can estimate:

```text
minimum readable angular size
        ↓
visual acuity
        ↓
trend over time
```

And track:

```text
           Visual acuity

1.0 ┤                    ╭──
0.9 ┤              ╭─────╯
0.8 ┤        ╭─────╯
0.7 ┤  ╭─────╯
    └────────────────────────
      Mar Apr May Jun Jul Aug
```

That is **far more defensible** than claiming the app can reverse myopia.

---

### 4. Then add the LLM layer

This is where your background is particularly useful.

Instead of building another static health app, make it an **AI vision scientist for one person**.

The user says:

> “I've been using -1.5D glasses for computer work for 3 months.”

The agent has their entire longitudinal dataset:

```text
Prescription
Working distance
Screen time
Outdoor time
Sleep
Symptoms
Visual acuity tests
Glasses configuration
```

Then:

```text
USER
Why did my right eye get worse this month?

AGENT

Your right-eye measurement changed from -4.25D
to approximately -4.50D.

But your measurement variance is ±0.25D,
so this isn't strong evidence of deterioration.

The notable change is actually:

Computer time:       +31%
Average distance:    58cm → 49cm
Barely-clear test:   61cm → 55cm

I'd repeat the standardized test 3 times
over the next 7 days before interpreting this.
```

**That is an AI-native product.**

The LLM isn't pretending to be an ophthalmologist. It's the interface over the user's experimental data.

---

### 5. Another potentially huge product: **AI Glasses Prescription Router**

Your page has an important product insight:

> **One prescription doesn't necessarily fit every activity.**

You explicitly divide use into things like driving versus phone/computer use, and discuss different lens configurations. ([Zhiwei Li][1])

Turn that into:

```text
                    What are you doing?

             ┌──────────┼───────────┐
             ▼          ▼           ▼
          Driving    Computer     Reading
             │          │           │
             ▼          ▼           ▼
          FULL RX     NEAR RX      NEAR RX
```

The app remembers:

```text
Driving glasses
Computer glasses
Reading glasses
Outdoor glasses
```

and tells the user:

> **You're about to start a 4-hour coding session.**

> Recommended pair: `Computer`

Potentially later:

**smart glasses / Ray-Ban / camera wearable integration**

could make this much more automatic. Camera-based AI visual assistants are already becoming a real product category; for example, current products combine camera vision, voice interaction, OCR and scene understanding. ([T3][2])

---

## 6. The really interesting long-term product: **Vision Lab**

I actually think this fits your personality better.

Not:

> “We cure myopia.”

Instead:

> **“Run controlled experiments on your own vision.”**

Something like:

```text
Vision Lab

Experiment #17
────────────────────────────

Question:

Does -1.50D undercorrection improve
my near-work comfort?

Protocol:

A: full prescription
B: -1.00D
C: -1.50D

Duration:
4 weeks

Measurements:

visual acuity
working distance
clarity threshold
eye fatigue
screen time
sleep
outdoor exposure

                 [ START ]
```

Then the system analyzes the data.

Eventually you could have:

```text
                  Personal Vision Model

                 ┌─────────────────┐
                 │      Vision     │
                 └────────┬────────┘
                          │
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼
  prescription       behavior           environment
       │                  │                  │
   glasses            screen time        outdoor time
   astigmatism        working distance   lighting
   acuity             near work          sleep
       │                  │                  │
       └──────────────────┼──────────────────┘
                          ▼
                  longitudinal model
                          │
                          ▼
                 personalized advice
```

That's much more defensible scientifically because the product is fundamentally **measurement + experimentation + longitudinal data**, rather than selling a medical conclusion.

And there is already research in 2026 exploring smartphone-based visual assistance and personalized object recognition, showing how far commodity phones + multimodal models can go. ([arXiv][3])

---

## What I would actually build

I'd **not** start with hardware.

I'd build this:

### `VisionLab`

```bash
visionlab test
visionlab log
visionlab prescription
visionlab experiment
visionlab report
```

Mobile UI can eventually sit on top of the same backend.

MVP:

```text
1. Enter prescription
2. Standardized visual-acuity test
3. Measure phone ↔ eye distance
4. Log glasses being used
5. Log screen/near-work sessions
6. Daily "barely clear" test
7. Plot prescription / acuity / distance over months
8. AI analyzes the personal time series
```

The **first killer screen** should probably be:

```text
VISION
────────────────────────

Today

Near-work                 5h 42m
Average distance           57cm
Outdoor                    1h 18m

Barely-clear distance      61cm
Previous                   57cm
                           ↑ 4cm

Visual acuity              0.9
Previous                   0.9

Prescription
L   -2.50 / -1.00
R   -4.25 / -1.25

────────────────────────
        Ask Vision AI
────────────────────────
```

Then the killer retention loop is simply:

**measure → experiment → observe → learn → repeat.**

One important change I'd make from the current page: **don't encode “myopia reversal” as a proven medical outcome.** Your own page acknowledges uncertainty around the optimal amount of undercorrection and competing views. ([Zhiwei Li][1]) A product can preserve your experimental philosophy while clearly separating *personal observations* from *clinically established facts*. That's also important because existing vision-assistance apps already operate in a medical/accessibility-adjacent space. ([apps.apple.com][4])

**In one sentence:**

> **Build Strava + Oura + an AI research assistant for eyesight—not another “myopia cure” app.**

That has a much bigger product surface: **personal measurement → behavioral feedback → longitudinal dataset → AI scientist → eventually adaptive glasses/wearables.**

[1]: https://lzwjava.com/vision-tips-en "Comfortable Daily Eyeglass Use at 1.50D Below Full Prescription"
[2]: https://www.t3.com/tech/gopro-action-cameras/insta360-go-ultra-gemini-ai-update-0826?utm_source=chatgpt.com "Free software update turns Insta360's tiny action camera into a full-fledged AI assistant that can do things most smart glasses can't"
[3]: https://arxiv.org/abs/2607.16750?utm_source=chatgpt.com "VisionAssist: An Open-Source Smartphone Assistant for AI-Based Visual Accessibility"
[4]: https://apps.apple.com/us/app/visionai-visual-assistance/id6740747405?utm_source=chatgpt.com "‎VisionAI: visual assistance App - App Store"