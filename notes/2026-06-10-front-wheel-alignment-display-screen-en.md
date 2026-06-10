---
audio: false
generated: true
image: false
lang: en
layout: post
title: Front Wheel Alignment Display Screen
translated: false
type: note
---

**Question:** What is this screen, and how does it display the car's wheel alignment adjustments?

**Answer:**

This is a **3D/CCD wheel alignment machine display** (brand: Aurora 奥拉, a common Chinese alignment system). The title bar reads **前轮调整** — "Front Wheel Adjustment." It's showing live alignment angles for the front axle while a technician adjusts the suspension. The camera pods on the rail (top-left of your photo, the unit with the LED ring) optically track reflective targets clamped to each wheel and compute the wheel's 3D orientation in real time.

The screen is split: **left column = left front wheel, right column = right front wheel**, with three rows of angles:

**1. 后倾角 (Caster) — top row.** The fore/aft tilt of the steering axis. Both boxes show `----` because caster can't be measured statically — it requires a steering sweep (turning the wheel lock-to-lock so the system can solve the steering axis geometry). The spec range printed below is roughly 4°34′–5°34′.

**2. 外倾角 (Camber) — middle row.** The inward/outward tilt of the wheel viewed from the front.

- Left wheel: **1°22′** on a **red** background → out of spec (positive camber, leaning out too much). Scale shows the acceptable band around 10′–50′ negative.
- Right wheel: **−17′** on **green** → within spec.
- Center readout 1°39′ is the **camber difference** between sides — a big left/right split like this causes the car to pull toward the side with more positive camber.

**3. 前束 (Toe) — bottom row.** Whether the wheels point inward (toe-in) or outward (toe-out) viewed from above.

- Left: **1°5′**, red → way out (spec is roughly 0′–10′ per wheel). This much toe error scrubs tires fast — visible as feathered/sawtooth tread wear.
- Right: **3′**, green → fine.
- The number under the car diagram is **total toe** (sum of both sides).

**How the color coding works:** each value sits on a red–yellow–green–yellow–red bar. The little black marker (Ⅰ) shows where the current reading falls relative to the manufacturer's spec for the vehicle (selected in software — the bottom status bar shows the car model, an EV from 2021). Green = in tolerance, red = adjust. The technician turns tie rod ends (for toe) or adjusts strut/control-arm bolts (for camber) under the car and watches the numbers move live until everything goes green.

So in this snapshot: the **right front wheel is done**, the **left front wheel still needs both camber and toe corrected**, and caster hasn't been swept/measured yet. The yellow arrow icon at the bottom center is prompting the next step in the procedure.
