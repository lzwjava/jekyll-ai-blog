---
audio: false
generated: true
image: false
lang: en
layout: post
title: What is VLA in AI?
translated: false
type: note
---

Question: **What is the full name of VLA in AI?**

Answer: **VLA = Vision-Language-Action model**.

It is a class of AI models that combine:

* **Vision (V)** → understand images/video from cameras
* **Language (L)** → understand instructions, reasoning, and concepts through natural language
* **Action (A)** → output actions to control an agent, usually a robot

The basic pipeline:

```
Camera image
     |
     v
[ Vision Encoder ]
     |
     v
[ Multimodal Transformer / LLM ]
     |
User instruction:
"Pick up the red cup"
     |
     v
Action tokens
     |
     v
Robot controller
     |
     v
Motor commands
```

Compared with LLMs:

| Model                        | Input        | Output        |
| ---------------------------- | ------------ | ------------- |
| LLM                          | Text         | Text          |
| VLM (Vision-Language Model)  | Image + Text | Text          |
| VLA (Vision-Language-Action) | Image + Text | Robot actions |

Examples of VLA models:

* Google DeepMind **RT-2 (Robotics Transformer 2)**

  * Uses vision-language knowledge from large models and converts it into robot actions.
* Physical Intelligence **π0 (pi-zero)**

  * A general-purpose robot foundation model.
* NVIDIA **GR00T (Project GR00T)**

  * Humanoid robot foundation model.
* OpenAI robotics research has also explored multimodal embodied intelligence.

The key idea:

> A VLA is basically an **LLM for robots**: instead of generating the next text token, it generates the next physical action.

Technically, many modern VLAs are built by extending Transformer architectures:

```
image patches
      |
Vision Transformer (ViT)
      |
      +------ text tokens
      |
      v
Large Transformer
      |
      v
action tokens
      |
      v
trajectory / motor commands
```

A common training objective is:

[
P(a_t | I, L, a_{<t})
]

where:

* (I) = visual observation
* (L) = language instruction
* (a_t) = next action

Similar to GPT:

[
P(x_t | x_{<t})
]

but the predicted token is an **action token** instead of a word.

References:

* [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818?utm_source=chatgpt.com)
* [A Vision-Language-Action Model for General Robot Control (π0)](https://arxiv.org/abs/2410.24164?utm_source=chatgpt.com)
* [NVIDIA Project GR00T](https://www.nvidia.com/en-us/robotics/isaac/gr00t/?utm_source=chatgpt.com)
