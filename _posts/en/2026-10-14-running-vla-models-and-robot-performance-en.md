---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running VLA Models and Robot Performance
translated: false
type: note
---

**Question:** How do you run VLA (Vision-Language-Action) models, and how do robots actually perform with them?

---

**Answer:**

## What is a VLA Model?

A Vision-Language-Action model is an AI system that processes a camera feed, a natural language instruction, and the robot's own state, then outputs motor commands — with its vision, language, and action modules trained jointly and run in one forward pass, rather than as a classical perception-then-planning-then-control pipeline.

The three core components are:

- **Vision encoder** — processes raw camera frames (often from multiple cameras) using models like DINOv2 + SigLIP
- **Language backbone** — encodes instructions like "pick up the red block" using a pretrained LLM (e.g., LLaMA 2, PaliGemma)
- **Action decoder** — converts the fused representation into motor commands

---

## Key VLA Models (2026)

Here's a comparison of the major open models available today:

| Model | Parameters | Action Head | License | Hardware |
| ------- | ----------- | ------------- | --------- | ---------- |
| OpenVLA | 7B | Autoregressive tokens | MIT | A100/H100, or 24GB with 4-bit quant |
| Octo | 27M / 93M | Diffusion policy | MIT | Single RTX 4090 |
| pi0 / pi0.5 / pi0.6 | 3.3B | Flow matching | Open checkpoints | Multi-GPU or single A100 |
| Gemini Robotics 1.5 | Undisclosed | Hybrid cloud+edge | Closed | Cloud-tethered |
| SmolVLA | 450M | Flow matching | Apache 2.0 | RTX 3060, Jetson, or laptop CPU |

---

## How to Run VLA Models

### Option 1 — SmolVLA via LeRobot (easiest, runs on consumer GPU)

Install and fine-tune SmolVLA using HuggingFace's LeRobot framework:

```bash
# Install
git clone https://github.com/huggingface/lerobot.git
cd lerobot
pip install -e .[smolvla]

# Fine-tune on your dataset
python lerobot/scripts/train.py \
  --policy.path=lerobot/smolvla_base \
  --dataset.repo_id=lerobot/svla_so101_pickplace \
  --batch_size=64 \
  --steps=20000 \
  --policy.device=cuda

# Run on a real robot
python -m lerobot.record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --dataset.single_task="Grasp a lego block and put it in the bin."
```

### Option 2 — OpenVLA (research baseline)

OpenVLA supports LoRA fine-tuning and 4-bit quantization. A quantized version fits on a 24GB RTX 4090. It beat the closed RT-2-X model by 16.5 percentage points of task success across 29 tasks, despite RT-2-X having 55B parameters vs OpenVLA's 7B.

### Option 3 — pi0 / openpi (best dexterity)

The openpi repository contains checkpoints and an approximate training pipeline, pretrained on more than 10,000 hours of robot data. Best for bimanual or contact-rich tasks.

---

## How Do Robots Perform?

**Strengths:**

- VLAs generalize better to conditions they were never explicitly trained on, because the underlying VLM backbone already knows what a mug, a towel, or a drawer looks like from web-scale pretraining before it ever saw a robot demonstration.
- pi0 demonstrated bimanual tasks such as folding laundry, packing groceries, and assembling boxes with a level of dexterity nothing before it had shown.
- Gemini Robotics 1.5 achieved motion transfer — a skill trained on one robot platform carried over directly to a different robot and a humanoid, without retraining.

**Limitations:**

- Mid-task recovery is inconsistent — when a grasp slips halfway through, or an object shifts, the model struggles because most demonstration data only captures successful attempts.
- Getting a 7B+ parameter model to run at 10–100Hz on the robot's own hardware is still mostly unsolved. Most deployed systems either tether to an edge server or split reasoning from control.
- Current VLAs generalize well inside their training distribution and degrade noticeably outside it.

**Choosing a model:**

- Consumer GPU / hobby arm → **SmolVLA**
- Bimanual / dexterous tasks → **pi0**
- Research baseline → **OpenVLA**
- Compute-constrained → **Octo**
- Frontier proprietary → **Gemini Robotics 1.5** (not self-hostable)

---

**References:**

- [Vision-Language-Action Models Explained (DataCamp, Sep 2026)](https://www.datacamp.com/tutorial/vision-language-action-models-explained)
- [SmolVLA on HuggingFace / LeRobot](https://huggingface.co/lerobot/smolvla_base)
- [openpi repository — pi0 checkpoints](https://github.com/Physical-Intelligence/openpi)
- [OpenVLA project page](https://openvla.github.io/)
