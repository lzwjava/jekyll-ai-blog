---
audio: false
generated: true
image: false
lang: en
layout: post
title: Modern Parking Systems Ignore Dry Steering Damage
translated: false
type: note
---

**Question:** Your friend says: modern smart-parking systems don't know to move the car slightly before turning the steering wheel — why don't they protect the chassis this way?

**Answer:**

Your friend is talking about **dry steering** (原地打方向盘 / 静态转向) — turning the steering wheel while the car is stationary. Here's why it matters and why autopilot systems sometimes do it anyway.

---

## The Physics

When you turn the steering wheel with the car stopped:

- The tire contact patch is fully loaded (full vehicle weight)
- The tire must **scrub/drag sideways** across the pavement instead of rolling
- This creates massive lateral force on:
  - **Tie rods** (连杆)
  - **Ball joints** (球头)
  - **Steering rack** (转向齿条)
  - **Wheel bearings** (轮毂轴承)

The correct technique: **creep forward or backward a few cm first**, so the tire rolls while turning — distributing the stress across the rolling motion instead of grinding stationary rubber against asphalt.

---

## Why Do Auto-Parking Systems Still Dry Steer?

A few reasons:

**1. Control model simplicity**
Most auto-parking uses a **kinematic bicycle model** — it optimizes for geometric path accuracy, not mechanical wear. The steering angle command is computed independently of whether the wheels are rolling. Moving slightly before steering adds state complexity.

**2. Space constraints in the parking algorithm**
The planner is trying to fit into a tight space. Adding "must have velocity > 0 before steering delta" as a constraint tightens the feasible solution space and can make parking fail more often.

**3. Electric Power Steering (EPS) makes it easy to ignore**
With EPS, the driver/system feels zero resistance when dry steering. In old hydraulic setups you *felt* the resistance. EPS hides the mechanical cost → engineers deprioritize it.

**4. No feedback signal for chassis wear**
The car has no sensor that measures tie rod stress or bearing fatigue. So the optimization loop has no cost function term for this damage — it literally cannot learn to avoid it.

**5. Liability/certification focus**
Automakers certify AEB, lane keeping, collision avoidance. Chassis wear from parking style is a 5–10 year diffuse cost, not a crash. No regulation forces them to care.

---

## Your Friend Is Right

Dry steering absolutely accelerates wear on:
- Ball joints → looseness, clunking
- Tie rod ends → steering play
- Tires → uneven shoulder wear

The fix is trivial in the control algorithm — add a small velocity pre-condition before large steering angle changes. Some premium systems (Bosch's latest parking stack, some BMW implementations) do handle this. Most mid-range systems don't bother.

It's a case of **optimization target mismatch**: the system is optimized for "park successfully in N seconds" not "minimize mechanical wear over vehicle lifetime."