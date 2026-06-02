---
audio: false
generated: true
image: false
lang: en
layout: post
title: Limits of Visual Math Reasoning
translated: false
type: note
---

Question:
Is the paper suggesting a two-step pipeline (image → text → math reasoning), meaning there is no real image-based reasoning, and instead it might rely on OCR + RLHF-style training after converting images?

Answer:

Short answer: **Yes — your interpretation is mostly correct.**
But the deeper truth is:

* Many current systems **do exactly image → text → reasoning**
* True **native visual reasoning** is still weak
* The paper you shared actually **shows this limitation explicitly**

---

## What the paper is actually about

Your link corresponds to **MathGen**, which evaluates whether models can **do math when answers must be visual (diagram / layout)** instead of text.
The key finding:

* Models that are strong at text math **fail badly** when required to output **visual math**
* Even best closed models only reach **~42%**
* Open models drop to **~1–11%** accuracy
  This shows **visual math reasoning is still a bottleneck**. ([Hugging Face][1])

So the paper is basically saying:

> current models don't really "reason in image space"

They mostly reason in **language space**.

---

## The two-step pipeline you described

This is indeed the dominant architecture:

```
Image
  ↓
Vision encoder (ViT / CNN)
  ↓
latent tokens
  ↓
text-like representation
  ↓
LLM reasoning
  ↓
text answer
```

So internally it's basically:

```
image → pseudo text → reasoning
```

Not true "visual thinking".

---

## Why this happens

Because:

* LLM reasoning circuits live in **token space**
* Vision encoder just converts pixels → tokens
* Reasoning happens **after conversion**

So the model isn't manipulating shapes — it's manipulating **descriptions of shapes**.

Example:

Image: triangle with angles
Model internally becomes:

```
"triangle ABC angle A = 30 ..."
```

Then standard math reasoning.

---

## What would be real image reasoning

True visual reasoning would look like:

* rotate shapes
* extend lines
* measure intersections
* simulate geometry

like a **differentiable CAD engine** inside the model.

Almost no model does this yet.

---

## RLHF after image?

You asked:

> or RLHF after image?

Yes — modern pipelines often do:

1. multimodal pretraining
2. supervised fine-tuning on image+text
3. RLHF / RLAIF on multimodal tasks

But this **still doesn't create visual reasoning**, only improves:

* OCR accuracy
* grounding
* answer formatting

Not real spatial reasoning.

---

## There ARE attempts to fix this

Research directions:

### 1. caption-assisted reasoning

convert image → caption → reason (still 2-step)

### 2. visualization-of-thought

model generates intermediate diagrams

### 3. world-model / latent reasoning

reason directly in visual latent space

### 4. tool-augmented

use geometry solver / python / renderer

These are still early.

---

## Final conclusion

You're basically correct:

* current systems mostly **image → text → reasoning**
* not true image reasoning
* RLHF only improves alignment
* paper shows visual math ability still weak
* real multimodal reasoning still unsolved

So yes — **your intuition is right.**

[1]: https://huggingface.co/papers/2603.27959?utm_source=chatgpt.com "Paper page - MathGen: Revealing the Illusion of Mathematical Competence through Text-to-Image Generation"
