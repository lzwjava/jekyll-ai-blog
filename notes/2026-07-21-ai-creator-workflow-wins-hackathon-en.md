---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Creator Workflow Wins Hackathon
translated: false
type: note
---

Question: How to win the AMD Radeon Hackathon Track 1 (Multimodal AI) with a strong project strategy?

Answer:

For Track 1, the judges are giving **80% to product value + innovation** and only **20% to Radeon GPU performance**. So don't build "just another Stable Diffusion UI". The winning strategy is:

> Build a complete AI creator workflow that solves a real problem, then prove it runs efficiently on AMD Radeon.

Think **AI-native product**, not model demo.

## Winning project idea: "AI Video Factory for Creators"

A pipeline:

```
Idea / Script
      |
      v
LLM Story Planner
      |
      v
Text -> Image (scene generation)
      |
      v
Image -> Video (motion generation)
      |
      v
Voice Generation
      |
      v
Auto Subtitle + Editing
      |
      v
Final Shorts/Reels/TikTok video
```

One click:

```
"Create a 30 second Tesla AI news video"
```

Output:

* storyboard
* images
* animated video
* narration
* captions
* thumbnail

This matches:

* text-to-image ✅
* image editing ✅
* image-to-video ✅
* audio generation ✅
* creator application ✅

---

## Why this can beat competitors

Most hackathon submissions will be:

* Stable Diffusion wrapper
* chatbot with image generation
* simple ComfyUI workflow

Those are commodity.

Your differentiation:

### "AI Content Factory"

Target:

* YouTubers
* TikTok creators
* marketing teams
* solo entrepreneurs

Problem:

> Creating daily video content requires 3-5 hours.

Solution:

> Generate 10 shorts/day from one idea.

---

# Architecture

## Frontend

Simple:

```
React
 |
 |
FastAPI
 |
 |
Workflow Engine
```

---

## AI pipeline

### 1. LLM Planner

Input:

```
Topic:
"Explain AMD MI300X"
```

Output:

```json
{
 "scenes":[
   {
    "duration":5,
    "image_prompt":
    "AMD MI300X GPU inside datacenter"
   }
 ]
}
```

Models:

* Qwen
* Llama
* DeepSeek

---

### 2. Text -> Image

Use:

* Stable Diffusion XL
* FLUX
* SD3

Example:

```
prompt
 |
v
diffusion model
 |
v
1024x1024 image
```

---

### 3. Image -> Video

This is where you win.

Use:

* Stable Video Diffusion
* AnimateDiff
* CogVideoX
* Wan2.1

Pipeline:

```
image
 |
encoder
 |
temporal transformer
 |
video frames
```

Generate:

```
1 image

↓

16-24 frames

↓

mp4
```

---

### 4. Audio

Use:

* Whisper
* XTTS
* CosyVoice

---

# Radeon optimization section (20 points)

This is important.

Don't just say:

"Runs on AMD"

Show benchmarks.

Example:

Hardware:

```
RX 7900 XTX
24GB VRAM
ROCm
```

Measure:

```
Model              GPU       Time

SDXL               Radeon    18s/image

SDXL               CPU       4min/image


Video generation:
SVD
24 frames
45 seconds
```

Create dashboard:

```
AMD Radeon AI Performance

VRAM:
18.2GB / 24GB

GPU utilization:
96%

Generation:
2.1 sec/frame
```

Judges love visible engineering.

---

# Even stronger: build an agent

Instead of fixed workflow:

```
Creator Agent

User:
"make a video about Nvidia vs AMD"


Agent:

1. research topic
2. write script
3. create images
4. animate
5. generate voice
6. edit video
7. publish
```

This connects with current AI trend.

---

# Suggested tech stack

```
Frontend:
Next.js


Backend:
FastAPI


Agent:
LangGraph / custom


Image:
Diffusers


Video:
ComfyUI backend


Audio:
XTTS


Acceleration:
ROCm
PyTorch AMD build
ONNX Runtime
```

---

# Demo scenario (very important)

Don't demo:

"Here is my model."

Demo:

Start timer:

```
Input:

"Create a 30 second AI news video:
AMD releases new GPU"


0 sec

Agent starts


20 sec

Storyboard ready


60 sec

Images generated


120 sec

Video generated


180 sec

Final MP4
```

Then play output.

Judges remember outcomes.

---

# Extra points: use your own advantage

Given your background, I would make it:

## "AI Research-to-Video Factory"

Because you already have:

* thousands of AI notes
* blog pipeline
* video generation workflow
* AI experiments

Demo:

```
Your blog markdown

        |
        v

AI reads article

        |
        v

Creates:

- YouTube short
- Bilibili video
- WeChat video
- thumbnail
- subtitles
```

This is a real product, not a hackathon toy.

---

# 48-hour implementation plan

## Day 1 morning

Build:

```
Markdown
 |
LLM
 |
Storyboard JSON
```

## Day 1 afternoon

Integrate:

```
SDXL
+
AnimateDiff
```

## Day 1 night

Add:

```
voice
subtitle
video merge
```

## Day 2

Polish:

* UI
* Radeon benchmark
* demo video
* README

---

# Winning pitch

Title:

> Radeon Creator AI Studio: An Autonomous Multimodal Agent for Generating Professional Short Videos

One sentence:

> "We turn one idea into a complete publish-ready video using AMD Radeon accelerated multimodal AI models."

---

References:

* AMD ROCm documentation: [https://rocm.docs.amd.com/](https://rocm.docs.amd.com/)
* Hugging Face Diffusers: [https://huggingface.co/docs/diffusers](https://huggingface.co/docs/diffusers)
* ComfyUI: [https://github.com/comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)
* Stable Video Diffusion: [https://huggingface.co/docs/diffusers/en/using-diffusers/svd](https://huggingface.co/docs/diffusers/en/using-diffusers/svd)
* Luma AI: [https://lumalabs.ai/](https://lumalabs.ai/)
