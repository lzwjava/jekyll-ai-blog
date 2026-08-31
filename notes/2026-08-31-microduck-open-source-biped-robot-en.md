---
audio: false
generated: true
image: false
lang: en
layout: post
title: Microduck Open-Source Biped Robot
translated: false
type: note
---

**Question:** What is the `microduck` project on GitHub?

**Answer:**

**Microduck** is an open-source, tiny biped duck robot 🦆 built by [Pollen Robotics](https://pollen-robotics.com/microduck). Here's a breakdown:

**What it is**

It is a tiny biped robot that moves using reinforcement learning policies. About 25 cm tall and 800 g, it runs on a Rockchip RK3566 SoC, with a 50 Hz control loop driving fifteen servos from neural policies, radios, a camera, and an update system that can push new software without bricking the device.

**What it can do**

- Walk (gamepad-controlled)
- Roll (with wheels swapped on)
- Pick things up (beak to floor, one button)
- Stand itself back up after being knocked over
- Kick a ball, sit, quack, and more

**How it's built — under the hood**

It's written in Rust, with no framework, as one workspace. Key daemons include: `robotd` (control loop and motor bus), `updaterd` (installs signed releases and rolls back on failure), `configd` (wifi and identity), `btd` (Bluetooth path for phones), `padd` (gamepad input), `mediad` (WebRTC camera stream), and `tofd` (depth sensor). They all communicate over a shared JSON-RPC contract on Unix sockets — every client (app, console, gamepad, scripts) sends the same calls.

**The AI / policy side**

The policies are trained in the companion repo `microduck_rl` using MuJoCo and PPO (a reinforcement learning algorithm), with domain randomization for sim-to-real transfer, and exported to ONNX format which this repo then loads.

**Who it's for**

The repo serves two audiences: people who own a Microduck (cheat sheet, gamepad setup, updates) and developers who want to build on it or train new policies.

---

**References:**
- [pollen-robotics/microduck — GitHub](https://github.com/pollen-robotics/microduck)
- [microduck_rl (policy training repo)](https://github.com/pollen-robotics/microduck_rl)
- [Architecture overview](https://github.com/pollen-robotics/microduck/blob/main/docs/design/architecture.md)
