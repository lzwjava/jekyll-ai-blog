---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minimal Path to Vision-Only Autonomous Driving
translated: false
type: note
---

**Question:** What's the minimal viable path to explore end-to-end autonomous driving like Tesla/openpilot — vision-only, no LiDAR, runs on accessible hardware?

**Answer:**

You're thinking exactly right. Let me break this down.

## openpilot's Architecture (is it really end-to-end?)

openpilot is **partially** end-to-end. It has two main neural nets:

```
Camera frames → [Supercombo model] → driving trajectory + lane lines + lead car
trajectory → [lateral/longitudinal controllers] → steering/throttle/brake
```

The `Supercombo` model is a CNN+transformer hybrid (Vision Transformer backbone since ~2022). But the **control layer is still classical** — PID/MPC controllers convert trajectory to actuator commands.

So: **perception is learned, control is classical**. Not fully E2E like Tesla's recent FSD v12 which outputs actuator commands directly.

**Tesla FSD v12** (2024) is the real E2E shift — video in, steering/throttle out, massive transformer. Wayve, NVIDIA DriveE2E are similar.

**Xpeng/Li Auto** — yes, they both shifted to transformer-based E2E perception around 2023-2024, similar to UniAD/VAD architectures from academia.

---

## Your Minimal Viable Exploration Path

You don't need a car. Here's the ladder:

### Level 1: Pure software — replicate openpilot's perception

```python
# Use comma.ai's dataset (comma2k19, ~33 hours of driving)
# https://github.com/commaai/comma2k19

# Run supercombo ONNX model on a driving video
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("supercombo.onnx")
# Input: [batch, 12, 128, 256] — 2 frames, YUV420
# Output: trajectory, lane lines, lead car
```

comma.ai releases the model weights. You can run inference on any dashcam footage.

### Level 2: Phone as sensor (your idea — excellent)

```
Phone camera → frame capture → MobileNet/YOLO → lane detection + depth
           → simple path planning → display overlay
```

This is exactly what **openpilot on phone** experiments do. There's `openpilot-on-laptop` repos. Phone gives you:

- 30fps camera
- IMU (gyro/accel) — critical for motion estimation
- GPS

### Level 3: The Zhihui Jun route — self-driving bicycle/cart

Zhihui Jun used a bicycle with:

- Raspberry Pi / Jetson Nano
- Camera
- Servo for steering

Minimum hardware:

```
Jetson Orin Nano ($250)
+ USB camera or Pi camera
+ RC car chassis (~$50)
+ PWM servo controller
```

This is actually the best learning path — you get real actuation feedback.

### Level 4: True E2E (what you should ultimately build toward)

```python
# Input: sequence of camera frames (like Tesla)
# Output: [steering_angle, throttle, brake]

# Architecture: Video Transformer (similar to Gato/RT-2)
class E2EDriver(nn.Module):
    def __init__(self):
        self.backbone = ViT(...)       # frame encoder
        self.temporal = Transformer(...)  # sequence modeling
        self.head = MLP(out=3)         # steer, throttle, brake

    def forward(self, frames):  # [B, T, C, H, W]
        tokens = self.backbone(frames)
        context = self.temporal(tokens)
        return self.head(context[:, -1])  # last token
```

Train on imitation learning (BC) first, then add DAgger or RLHF.

---

## Data

The key bottleneck is data, not model architecture:

- **comma2k19** — free, 33h, highway US
- **nuScenes** — multi-sensor, good for research
- **Waymo Open Dataset** — high quality
- **Your own dashcam** — most relevant for your use case

---

## Recommended Stack for Your Exploration

```
Phase 1 (this week):
  - Download comma2k19
  - Run supercombo.onnx on sample frames
  - Visualize trajectory outputs

Phase 2 (next month):
  - Build phone → frame streamer → laptop inference pipeline
  - Implement lane detection with ONNX or torch

Phase 3 (hardware):
  - RC car + Jetson Orin Nano
  - Train small imitation learning model on your own driving data
  - Close the loop: camera → model → servo
```

---

## Key Papers to Read

- **UniAD** (2023) — "Planning-oriented Autonomous Driving", NeurIPS best paper
- **VAD** — Vectorized scene representation for E2E
- **Wayve GAIA-1** — generative world model for driving
- **Tesla FSD v12 blog** — E2E actuator-level control

---

Your instinct is right — vision-only E2E on a cheap platform is the Tesla philosophy, and it's the most learnable path. The RC car / self-driving bicycle is genuinely the best MVE (minimum viable experiment) for someone at your level. You'll learn more from closing the perception→action loop on a toy than reading 10 papers.

**References:**

- [comma.ai supercombo model](https://github.com/commaai/openpilot)
- [comma2k19 dataset](https://github.com/commaai/comma2k19)
- [UniAD paper](https://arxiv.org/abs/2212.10156)
- [openpilot on laptop experiments](https://github.com/commaai/openpilot/tree/master/tools)
