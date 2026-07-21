---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD AI DevMaster Hackathon 2026 Rules
translated: false
type: note
---

Question: **What is this AMD AI DevMaster Hackathon document?**

Answer:

This is the rule/specification document for the **AMD AI DevMaster Hackathon 2026**. It is a competition sponsored by AMD where developers build AI applications optimized for **AMD Radeon GPUs + ROCm**.

The core idea:

> Build something useful with AI, but make sure the heavy compute runs locally on AMD GPUs using ROCm.

There are **3 tracks**:

---

## Track 1 — Multimodal AI Content Creation (probably most relevant for you)

Build AI tools around:

* image generation
* image editing
* style transfer
* video stylization
* text-to-video
* image-to-video
* enhancement / upscaling
* batch content creation

Examples:

```
Input:
  photo/video/text prompt

GPU pipeline:
  Stable Diffusion / FLUX / ControlNet / LoRA
  + ROCm acceleration

Output:
  anime style video
  cyberpunk video
  marketing content
  short video generation
```

Required stack:

* AMD Radeon GPU from Radeon cloud
* ROCm
* PyTorch ROCm
* ComfyUI / Diffusers / Transformers allowed
* OpenCV / FFmpeg / Pillow allowed

Closed APIs cannot be the core. At least one key inference path must run locally on AMD GPU.

Deliverables:

* source code
* README
* PDF project description
* 3–5 min demo video

---

## Track 2 — Private Local AI Agent (also very suitable for you)

Basically:

> Build a local ChatGPT-like agent running on AMD GPU.

Examples:

* personal assistant
* coding agent
* knowledge base agent
* document/email assistant
* life management agent

Required capabilities:

At least **2 of these 5**:

1. RAG
2. Tool calling
3. Multi-step planning
4. Local memory
5. Permission/privacy control

Possible architecture:

```
                User
                 |
             Web UI / CLI
                 |
             Agent Router
                 |
       +---------+---------+
       |                   |
    Local LLM          Tools
   Qwen/Llama          |
       |               |
   ROCm/vLLM       Browser
                   Files
                   Git
                   Calendar

        AMD Radeon GPU
```

Recommended:

* vLLM
* llama.cpp
* Transformers + PyTorch ROCm
* LangChain/LlamaIndex/Dify/etc.

Given your existing `ww`, `iclaw`, agent experiments, this track maps very closely.

---

## Track 3 — Physical AI / Robotics

Robotics simulation:

* robot arms
* humanoids
* quadrupeds
* autonomous driving

Using:

* Genesis
* MuJoCo
* LeRobot
* OpenVLA

Need simulation + AI control + AMD GPU acceleration.

Probably less aligned unless you want to enter robotics.

---

## Prize

Each track:

| Place |  Prize |
| ----- | -----: |
| 1st   | $5,000 |
| 2nd   | $3,500 |
| 3rd   | $1,500 |

---

## Timeline

Important dates:

* Registration opened: July 10, 2026
* Submission opened: July 15, 2026
* Deadline: August 6, 2026 23:59 Beijing/Singapore time

---

## My recommendation for you

Given your background:

* GPT-2 training
* nanoGPT
* agent CLI tools
* blog/video automation
* AMD ROCm interest

I would choose **Track 2**.

A strong project idea:

# "OpenClaw Local AI Agent"

```
AMD Radeon GPU
        |
     Qwen3 / Llama
        |
   Agent Runtime
        |
 +------+-------+
 |      |       |
RAG   Tools   Memory
 |      |       |
Blog  Git    Vector DB
PDF   Shell  SQLite
Video
```

Demo:

1. User asks:

   > "Create today's AI research video"

2. Agent:

```
search papers
      |
summarize
      |
generate markdown
      |
generate image
      |
generate video
      |
publish
```

Everything local on AMD GPU.

This directly demonstrates:

* local inference
* tool calling
* workflow orchestration
* practical value

The judges explicitly score these capabilities.

For winning, don't build another chatbot. Build a **personal AI operating system running on Radeon**.
