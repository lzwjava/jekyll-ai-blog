---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multimodal LLM Training Pipeline
translated: false
type: note
---

Question: How can I train a multimodal model for a large language model (LLM)?

Answer:

Training a multimodal LLM (e.g., text + image, or text + audio + video) is basically about **connecting a pretrained modality encoder with a language model and training them to align in a shared representation space**.

Here is a practical, modern pipeline used in systems like GPT-4V-style models, LLaVA, Flamingo, etc.

---

## 1. Overall Architecture

A typical multimodal LLM has 3 parts:

### (1) Modality Encoder (frozen or lightly trained)

* Image: ViT (Vision Transformer), CLIP-ViT
* Audio: Whisper encoder / wav2vec
* Video: TimeSformer / VideoViT

Example:

* `image → ViT → 1024-d embeddings`

---

### (2) Projection / Adapter Layer

This maps modality embeddings into the LLM embedding space.

Common designs:

* Linear layer
* MLP (2–3 layers)
* Perceiver Resampler (Flamingo-style)
* Q-Former (BLIP-2 style)

Example:

```
vision_features (2048) → projector → 4096 (LLM hidden size)
```

---

### (3) Language Model (decoder)

* LLaMA / Qwen / Mistral / GPT-style decoder-only transformer
* Usually pretrained and partially frozen at first

---

## 2. Training Stages

### Stage A: Alignment Pretraining (most important)

Goal: teach model to “connect vision/audio → text tokens”

You train on paired data:

* image → caption
* image + question → answer
* video → description

Loss:

* standard next-token prediction (cross entropy)

Example:

```
Input: <image> "What is in the image?"
Target: "A dog running in a park"
```

---

### Stage B: Multimodal Instruction Tuning

Now you make it conversational:

Datasets:

* LLaVA-Instruct
* MiniGPT-4 data
* ShareGPT-style multimodal QA
* synthetic GPT-generated captions + QA

Goal:

* follow instructions involving images/audio

---

### Stage C: Optional Reinforcement Learning (RLHF / DPO)

* Improve reasoning quality
* Reduce hallucination
* Align responses with human preference

---

## 3. Data Requirements

You need large-scale paired datasets:

### Vision-language:

* LAION-5B (filtered)
* COCO captions
* CC3M / CC12M
* Synthetic GPT captioning

### Instruction data:

* GPT-generated image QA pairs
* Human annotated VQA datasets

Key idea:

> Quality matters more than size for instruction tuning stage.

---

## 4. Common Training Recipes (modern practice)

### Option 1: LLaVA-style (simplest)

* Freeze vision encoder
* Freeze LLM (or partial LoRA)
* Train only projection layer first
* Then instruction fine-tune full system

---

### Option 2: BLIP-2 style

* Frozen vision encoder
* Train Q-Former (bridge module)
* Frozen LLM

Very efficient for limited compute.

---

### Option 3: Flamingo-style

* Cross-attention blocks inserted into LLM
* Train gated cross-attention layers
* Strong performance but more complex

---

## 5. Loss Functions

Main loss:

* next token prediction (causal LM loss)

Optional:

* contrastive loss (image-text alignment like CLIP)
* ranking loss (for VQA correctness)
* preference loss (DPO/RLHF)

---

## 6. Minimal PyTorch Concept

High-level flow:

```python
image_features = vision_encoder(image)
projected = projector(image_features)

text_embeddings = tokenizer(text)

inputs = concat(projected, text_embeddings)

loss = language_model(inputs, labels)
loss.backward()
```

---

## 7. Key Engineering Challenges

### (1) Alignment instability

* vision embeddings collapse if projector is too weak

### (2) Tokenization mismatch

* need special “image tokens” or prefix embeddings

### (3) Overfitting to captions

* model becomes “caption bot” instead of reasoning

### (4) Compute cost

* multimodal training is memory-heavy (especially video)

---

## 8. Recommended Starting Stack (practical)

If you want to build one yourself:

* Vision encoder: `openai/clip-vit-large-patch14`
* LLM: `LLaMA 3 / Qwen2.5`
* Frameworks:

  * HuggingFace Transformers
  * DeepSpeed / FSDP
  * LLaVA repo (best reference baseline)

---

## 9. Best Learning Path

1. Train CLIP (image-text contrastive)
2. Train captioning model
3. Build LLaVA-style VQA system
4. Add instruction tuning
5. Scale to multi-image / video

---

If you want, I can also show:

* a **minimal working LLaVA training code**
* how to do it on **1× RTX 4070**
* or how GPT-style models do **image token injection internally**