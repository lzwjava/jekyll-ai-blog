---
audio: false
generated: true
image: false
lang: en
layout: post
title: SenseNova Multimodal Foundation Models
translated: false
type: note
---

Question: intro to SenseNova (Hugging Face organization)

Answer:

SenseTime's SenseNova is its foundation model family. The Hugging Face organization `sensenova` publishes open models around multimodal AI, vision-language models, image generation, and agent systems. ([Hugging Face][1])

Think of SenseNova as China's equivalent attempt at a **GPT-4o / Gemini-style multimodal foundation model stack**:

```
SenseNova
├── Language models
│   └── reasoning / chat / agents
│
├── Vision-language models
│   └── understand images + text
│
├── Unified multimodal models
│   └── input: text/image
│   └── output: text/image/mixed generation
│
├── Image generation
│   └── text → image
│   └── image editing
│
└── Agent ecosystem
    └── tools + workflows
```

([Sensenova][2])

## Company background

SenseNova comes from SenseTime (商汤科技), founded in 2014. SenseTime originally became famous for computer vision:

* face recognition
* autonomous driving perception
* smart city cameras
* industrial vision

Then after ChatGPT (2022), they shifted heavily toward foundation models:

```
Old SenseTime:
Computer Vision
       ↓
Deep learning perception models
       ↓
Industry AI

New SenseTime:
Large-scale compute
       ↓
Foundation models
       ↓
Multimodal agents
       ↓
Enterprise AI
```

([SenseTime][3])

---

## Interesting Hugging Face models

The HF organization currently contains models such as: ([Hugging Face][1])

### 1. SenseNova-U1

Example:

```
sensenova/SenseNova-U1-8B-MoT
```

This is their unified multimodal model.

MoT = Mixture of Tokens.

The idea:

Traditional:

```
Image
 ↓
Vision Encoder
 ↓
LLM
 ↓
Text answer
```

Unified model:

```
Image tokens
Text tokens
Audio/video tokens
       ↓
 Transformer
       ↓
Text tokens
Image tokens
```

Similar direction as:

* GPT-4o
* Gemini
* Chameleon
* BAGEL
* NEO-unify

SenseTime describes U1 as a unified understanding + generation model using its NEO-unify architecture. ([SenseTime][4])

---

### 2. SenseNova-Vision

Vision-language model:

```
image + question
        ↓
SenseNova-Vision
        ↓
answer
```

Examples:

Input:

```
<image>
What GPU is this?
```

Output:

```
This appears to be an NVIDIA RTX 4090...
```

Similar category:

* Qwen2.5-VL
* InternVL
* LLaVA
* GPT-4V

---

### 3. SenseNova-SI

Spatial intelligence models.

This is interesting because it moves from:

```
"what is in the image?"
```

to:

```
"what is the 3D relationship of objects?"
```

Example:

```
robot camera image

→
where is the cup?
how far?
can robot grab it?
```

This connects to embodied AI.

---

### 4. SenseNova-MARS

Reasoning-oriented multimodal model.

Direction:

```
Vision
+
Language
+
Reasoning
```

Similar trend:

* OpenAI o-series
* DeepSeek-R1
* Gemini thinking models

---

## Why SenseNova is interesting technically

The important shift:

Before:

```
Separate models

CLIP
 +
LLM
 +
Diffusion
 +
Speech model
```

Now:

```
One foundation model

          Transformer
        /     |      \
    text    image    action
```

The industry is moving toward **native multimodal models**.

Your previous experiments with:

* nanoGPT
* GPT-2 training
* FLUX
* Qwen-VL

are exactly touching this direction.

---

## How to run / study it

For example:

```bash
git clone https://huggingface.co/sensenova/SenseNova-U1-8B-MoT

pip install transformers accelerate

python inference.py
```

Conceptually:

```python
image = load_image("gpu.jpg")

tokens = processor(
    text="identify this GPU",
    image=image
)

output = model.generate(tokens)

print(output)
```

The interesting engineering parts:

1. multimodal tokenization

```
image
 ↓
patch embedding
 ↓
visual tokens
```

2. transformer attention

```
[text tokens]
      +
[image tokens]

      ↓

 self attention

      ↓

reasoning
```

3. unified generation

```
output:
"text"
or
"image tokens"
```

---

## Compared with Qwen / DeepSeek

A rough map:

| Model family | Main strength                       |
| ------------ | ----------------------------------- |
| Qwen         | open general LLM + multimodal       |
| DeepSeek     | reasoning + efficient training      |
| SenseNova    | vision + multimodal + enterprise AI |
| InternVL     | strong vision-language research     |
| GPT-4o       | closed multimodal product           |

SenseNova's historical advantage is **computer vision**, so their bet is:

```
Vision AI expertise
        +
Large language models
        +
Agents
        =
Physical-world AI
```

([SenseTime][5])

For someone like you who likes **GPU repair + hardware + AI**, SenseNova's direction is actually very relevant: the future "AI engineer" stack is likely not only training transformers, but connecting:

```
camera
 ↓
multimodal model
 ↓
reasoning
 ↓
robot/tool/action
 ↓
physical world
```

References:

* SenseNova Hugging Face models: ([Hugging Face][1])
* SenseTime overview: ([SenseTime][3])
* SenseNova model platform: ([Sensenova][6])

[1]: https://huggingface.co/sensenova/models?utm_source=chatgpt.com "sensenova (SenseNova)"
[2]: https://www.sensenova.ai/models?utm_source=chatgpt.com "Models — SenseNova Multimodal AI Model Platform"
[3]: https://www.sensetime.com/en/about-index?utm_source=chatgpt.com "About SenseTime | SenseTime"
[4]: https://sensetime.com/en/news/51170625/?utm_source=chatgpt.com "SenseTime Fully Open-Sources SenseNova U1: A Unified Model for Understanding and Generation | SenseTime"
[5]: https://sensetime.com/en/?utm_source=chatgpt.com "SenseTime | SenseNova Multimodal LLM & AI Solutions"
[6]: https://www.sensenova.ai/?utm_source=chatgpt.com "SenseNova - Multimodal AI Model Platform"
