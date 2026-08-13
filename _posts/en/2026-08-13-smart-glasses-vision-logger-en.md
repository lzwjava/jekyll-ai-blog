---
audio: false
generated: true
image: false
lang: en
layout: post
title: Smart Glasses Vision Logger
translated: false
type: note
---

Question: **Can we build digital eyeglasses that continuously record what the user sees and learn how they use their vision—phone, computer, road, outdoors, etc.?**

Answer:

**Yes. And I think this is actually a much more interesting product than just a “vision app.”**

The key insight is: **you don't necessarily need to record everything. You need to turn the user's visual experience into structured events.**

Existing research has already demonstrated this direction. Tobii's research glasses, for example, combine inward-facing eye cameras with an outward-facing scene camera; research systems such as MemX combine visual attention with scene understanding to selectively capture meaningful moments. ([Frontiers][1])

And consumer hardware is getting close: Meta's current AI glasses already have a camera, onboard storage, phone integration and a capture LED. ([About Facebook][2])

### The architecture I'd build

```text
                    SMART GLASSES
                         │
          ┌──────────────┼──────────────┐
          │              │              │
      RGB camera     IMU / gyro     eye sensors
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                  phone / edge AI
                         │
                         ▼
                ┌─────────────────┐
                │ Scene classifier│
                └────────┬────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       PHONE          COMPUTER        ROAD
       2.5h            5.2h           1.1h
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  Vision Timeline
```

The important thing is that **the raw camera stream is not the product**.

The product is:

```text
08:12–08:34   📱 phone          22 min
08:34–10:51   💻 computer       2h 17m
10:51–11:20   🚶 outdoors       29 min
11:20–11:43   📱 phone          23 min
11:43–12:15   🍜 restaurant      32 min
12:15–12:42   🚗 driving         27 min
```

Then after a month:

```text
YOUR VISION PROFILE
──────────────────────────────

Near work                 6h 14m/day
Phone                     2h 03m/day
Computer                  4h 11m/day
Outdoor                   1h 47m/day
Driving                   0h 52m/day

Typical phone distance       38 cm
Typical computer distance    61 cm

Looking at near objects:
██████████████████████  71%

Looking far:
██████                  19%

Other:
███                     10%
```

**That's genuinely novel/useful data.**

---

## But I'd add one more sensor: eye tracking

This is the big difference between:

> **“camera attached to glasses”**

and

> **“a device that understands what your eyes are doing.”**

You want:

```text
             outward camera
                  │
                  ▼
            ┌───────────┐
            │ scene     │
            │ phone     │
            │ computer  │
            │ road      │
            └─────┬─────┘
                  │
                  │ correlate
                  │
            ┌─────▼─────┐
            │ eye gaze  │
            │           │
            │ left/right│
            │ fixation  │
            │ blink     │
            └───────────┘
```

Then you can distinguish:

```text
camera sees phone
        ≠
user is looking at phone
```

That's important.

Someone could be sitting next to a phone while looking at a person.

Eye tracking lets you ask:

> **Where is the user actually looking?**

There are already low-power research approaches to putting eye tracking into glasses. One 2024 system demonstrated non-invasive EOG-based tracking at very low power, with a reported 7.75 mW continuous acquisition and multi-day operation on a small battery. ([arXiv][3])

---

# You don't even need full eye tracking for V1

This is where I'd be pragmatic.

### V0

Use existing smart glasses.

```text
Ray-Ban Meta
      │
      │ camera
      ▼
phone
      │
      ▼
your app
```

Classify sampled frames:

```python
def classify(frame):
    return vision_model(
        frame,
        """
        classify the user's visual activity:
        phone, computer, reading, driving,
        walking, outdoors, person, TV, unknown
        """
    )
```

You don't need 30 FPS.

Sample:

```text
1 frame / 5 seconds
```

That's **720 frames/hour**.

But you probably don't even need that.

Use event detection:

```text
scene unchanged
     ↓
don't upload

scene changed significantly
     ↓
capture

new scene
     ↓
classify
```

You could reduce the data by 10–100×.

---

# And the AI should turn images into events

For example:

```json
{
  "start": "09:14",
  "end": "10:47",
  "activity": "computer",
  "confidence": 0.97,
  "estimated_distance_cm": 62
}
```

Then:

```json
{
  "start": "10:47",
  "end": "11:03",
  "activity": "walking_outdoors",
  "confidence": 0.94
}
```

Then your database becomes a **personal visual history** rather than a giant video archive.

---

# The killer feature is the longitudinal model

After 3 months:

```text
VisionLab AI

I've analyzed 1,284 hours of
visual activity.

Your biggest change:

Near-work increased 23%.

Average computer distance:
64 cm → 53 cm

Phone usage:
1h 21m → 2h 08m

Outdoor visual activity:
1h 54m → 1h 12m

Your visual-acuity measurements
did NOT change significantly.

I'd continue collecting data rather
than drawing a conclusion yet.
```

This is where your original **Vision Tips** idea becomes much more powerful.

You're no longer asking:

> “Is -1.50D better?”

You're building:

> **a longitudinal dataset of how a human actually uses their visual system.**

---

# There is an even crazier extension

Eventually:

```text
glasses
   │
   ├── camera
   ├── eye tracking
   ├── IMU
   ├── ambient light
   ├── distance estimation
   └── maybe pupil / EOG
          │
          ▼
      Vision Model
          │
          ▼
    Personal Vision OS
```

Then it can infer:

```text
                 Visual load

near ─────────────────────────────── far

       ███████████████████
       
       0–40cm    40–80cm    >80cm
```

And correlate that with:

```text
prescription
visual acuity
working distance
screen time
outdoor time
lighting
sleep
fatigue
head movement
blink rate
```

Now you have something approaching an **“Oura Ring for vision.”**

---

## One major product constraint: privacy

This is probably the hardest part.

A camera continuously recording what people around you are doing is fundamentally different from a smartwatch recording heart rate.

Meta explicitly uses a capture LED on its current AI glasses, and says it cannot be disabled. That's partly because people need to know when they're being recorded. ([About Facebook][2])

There are already significant privacy concerns around camera-equipped smart glasses in public. ([The Guardian][4])

So I'd make the architecture:

```text
             camera
                │
                ▼
          local inference
                │
                ▼
        structured events
                │
                ▼
        delete raw image
                │
                ▼
           phone/cloud
```

**Default: don't store the world. Store the user's visual statistics.**

That is a much better product philosophy.

---

# What I'd actually prototype

Don't manufacture glasses yet.

Use:

**existing camera glasses → phone → local VLM → SQLite → dashboard**

Something like:

```bash
visionlab ingest
visionlab classify
visionlab timeline
visionlab stats
visionlab report
```

And make the first dashboard:

```text
VISION LAB
────────────────────────────────

Today

📱 Phone             1h 47m
💻 Computer          5h 13m
📖 Reading           42m
🚗 Driving           51m
🌳 Outdoors          1h 32m
👀 Other             2h 08m

────────────────────────────────

Average viewing distance

Phone                37 cm
Computer             61 cm
Reading              43 cm

────────────────────────────────

7 day trend

Near work            +18%
Outdoor              -11%
Phone                 +7%

────────────────────────────────

[ Ask Vision AI ]
```

**Then**, once the software proves useful, build custom hardware around exactly the sensors you actually need.

The beautiful part is that **the first prototype is mostly software**. The hardware can initially just be a pair of camera glasses.

And this isn't science fiction: Meta's Project Aria Gen 2 already exists specifically as a glasses platform with multiple sensors, onboard machine perception and audio for researchers building machine-perception/AI applications. ([Meta AI][5])

My bet would be:

> **Don't build “digital eyeglasses.” Build a “Visual Activity Recorder” first.**

Then glasses become the sensor platform.

That makes the roadmap:

```text
V0   phone + existing glasses
 ↓
V1   Visual Activity Recorder
 ↓
V2   eye tracking
 ↓
V3   personal vision model
 ↓
V4   adaptive glasses
 ↓
V5   Vision OS
```

That is a **very AI-native hardware/software startup direction**.

[1]: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1607029/full?utm_source=chatgpt.com "Frontiers | Applying mobile eye tracking to measure real-time engagement and enhance informal learning at environmental exhibits"
[2]: https://about.fb.com/news/2026/07/metas-ai-glasses-your-questions-answered/amp/?utm_source=chatgpt.com "Meta’s AI Glasses: Your Questions Answered"
[3]: https://arxiv.org/abs/2412.14848?utm_source=chatgpt.com "ElectraSight: Smart Glasses with Fully Onboard Non-Invasive Eye Tracking Using Hybrid Contact and Contactless EOG"
[4]: https://www.theguardian.com/technology/2026/aug/08/ai-smartglasses-camera-film-privacy-consent?utm_source=chatgpt.com "This man was secretly snapped by someone with smartglasses. He's not alone in calling that a violation of privacy"
[5]: https://ai.meta.com/aria-application/?utm_source=chatgpt.com "Project ARIA Gen 2 Research Kit Application"
