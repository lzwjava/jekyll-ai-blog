---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mechanical vs Electrical Fan Buzz
translated: false
type: note
---

Question: A friend suggested checking whether the fan area has something touching it. Why would that matter?

Answer:

## Because "buzzing" has two completely different root causes, and you've only ruled out one

Your GPU-swap test ruled out an **electrical** source specific to the GPU (VRM inductor whine). But it does nothing to rule out a **mechanical** source — and a fan physically contacting something produces a sound that's easy to mistake for coil whine, especially if you're going by ear rather than isolating components.

Your friend's hypothesis is actually a good one to check first because it's the fastest, zero-cost test, and it's a very common false-positive for "coil whine":

### What mechanical contact sounds like and why it fools people

| Source | Mechanism | Sound signature |
| --- | --- | --- |
| Fan blade grazing a cable tie / sleeved cable | Blade tip flexes the cable on each rotation | Rhythmic buzz synced to fan RPM — pitch changes with fan speed |
| Fan blade hitting a dust bunny | Intermittent contact | Irregular buzz/rattle, may cut in/out |
| PSU/case fan hub loose on bearing | Fan motor vibrating against fan frame or grille | Continuous low buzz, changes with fan curve |
| Cable resting against a spinning fan from outside the shroud | Same as above but external | Buzz appears/disappears if you nudge the cable |
| CPU cooler fan wire routed too close to blades | Same | Ticking/buzzing tied to RPM |

The key diagnostic difference from real coil whine: **mechanical buzz scales with fan RPM** (get louder/higher-pitched as the fan spins faster under load, e.g. via GPU/CPU temps ramping up fan curves), while **coil whine scales with electrical load** (power draw), not fan speed. Since fan speed and power draw are correlated in a real workload, people conflate them constantly — this is exactly why your friend's advice is worth 30 seconds before doing PSU teardown tests.

### Quick check (do this before the PSU isolation test I gave you last time)

```bash
# No commands needed — physical inspection:
# 1. Open the case side panel
# 2. Visually trace every fan (case fans, CPU cooler fans, PSU fan if visible)
#    - Look for any cable, cable tie, or zip-tie tail crossing into the blade sweep radius
#    - Check the CPU cooler (AIO radiator fans especially — common culprit, wires often
#      routed right past the fan hub)
# 3. With power OFF, spin each fan by hand — feel for:
#    - Grinding vibration in the bearing (bad fan, needs replacement)
#    - Blade catching on anything as it passes a fixed point
# 4. With power ON, use a flashlight + strobe effect (or your phone's slow-mo camera)
#    to watch each fan's blade tips in real time — any wobble or contact will show up
#    immediately on video even if too fast to see live
```

If nothing is touching and fans spin freely by hand with no bearing grind, that's your confirmation to go back to the electrical isolation test (PSU paperclip test / VRM under load) from before — you'll have eliminated the cheap explanation first, which is the right order of operations for debugging (cheapest, fastest tests first, in your CS instincts this is just binary-search-by-cost rather than by evidence-quality).
