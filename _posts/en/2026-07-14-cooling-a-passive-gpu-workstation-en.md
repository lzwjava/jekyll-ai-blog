---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cooling a Passive GPU Workstation
translated: false
type: note
---

Question: What cooling setup does this build need?

Answer:

Two completely different cooling problems here — CPU and GPU — and the GPU one is the one people get wrong.

**CPU: R5 5600 stock cooler (Wraith Stealth) is undersized for sustained load.**

It's fine for gaming's bursty load but this is a workstation running sustained inference/training — closer to 100% duty cycle than gaming's variable load. Get a budget tower air cooler instead:

- Thermalright Peerless Assassin 120 SE or ID-Cooling SE-224-XT — both ~¥100-150, handle 65-95W TDP with headroom, quiet at sustained load
- Skip AIO liquid coolers here — no benefit for a 65W CPU, just adds a pump failure point for zero gain

**GPU: this is the real cooling problem. The MI50 is a passive card — it has zero onboard fans.**

Radeon Instinct cards are designed for server chassis with a wall of high-static-pressure fans pushing air axially through the heatsink fins. A normal ATX case's ambient airflow is nowhere near enough; without forced air directly through those fins, the card will thermal throttle or shut down under load within minutes.

You need one of:

1. **A 3D-printed fan shroud + high-static-pressure blower fan** mounted directly to the MI50's heatsink, ducting air through the fins — this is the standard hobbyist fix, widely documented for Instinct/Radeon Pro cards repurposed for desktop use. Search "MI50 fan shroud" or "MI25 blower mod" — printable STLs exist, plus pre-made adapter kits sold alongside these cards on Taobao/AliExpress for ~¥50-100.
2. **A high-CFM 40mm/60mm blower (e.g. Delta/Sunon server-grade blower, ~4000-6000 RPM)** zip-tied or bracket-mounted to blow directly across the card — noisier but simpler than sourcing/printing a shroud.

Don't skip this — it's not optional cooling, it's the difference between the card running at all under load versus throttling or shutting off within minutes.

**Case airflow (general):**

- mATX case with at least 2 intake + 1 exhaust fan, front-to-back or bottom-to-top positive pressure
- Since the MI50 needs its own dedicated blower anyway, case fans mainly need to clear ambient heat and feed the CPU cooler — a case like Fractal Meshify or similar mesh-front mATX case with 3x 120mm fans is enough
- Watch physical clearance: MI50 body + fan shroud can be long, check case GPU length spec (usually need 300mm+ clearance) before buying the case

**Concrete pick:** Thermalright Peerless Assassin 120 SE (CPU) + a printed/adapter fan shroud with a Delta-class 6000RPM blower for the MI50 + mATX mesh case with 3x120mm fans.

References:

- [MI50 real deployment: passive card requiring forced airflow](http://wtarreau.blogspot.com/2025/12/amd-radeon-instinct-mi50-32gb-best-ai.html)
- [MI50/MI25 fan shroud mod discussion](https://gist.github.com/evilJazz/14a4c82a67f2c52a6bb5f9cea02f5e13)
