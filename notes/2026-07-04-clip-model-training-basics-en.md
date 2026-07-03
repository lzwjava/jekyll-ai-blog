---
audio: false
generated: true
image: false
lang: en
layout: post
title: CLIP Model Training Basics
translated: false
type: note
---

Question: How do you train a CLIP (image-text contrastive) model?

Answer:

CLIP training is about learning a **shared embedding space where images and texts of the same meaning are close, and mismatched pairs are far apart**. It is one of the core building blocks behind modern multimodal LLMs.

---

## 1. Core Idea of CLIP

CLIP has two encoders:

* **Image encoder**: ViT / ResNet
* **Text encoder**: Transformer (like GPT encoder-style)

Both output vectors in the same dimension:

```
image → f_img → vector (d)
text  → f_txt → vector (d)
```

Then you compare them using cosine similarity.

---

## 2. Training Objective (Key Part)

You train on **(image, text) pairs**.

For a batch of N pairs:

* Each image should match its correct text
* All other texts are negatives
* All other images are negatives

---

### Similarity matrix

For batch size N:

```
S_ij = cosine_similarity(image_i, text_j)
```

You get an N×N matrix.

---

### Loss function (symmetric cross-entropy)

You do two directions:

#### (1) Image → Text

Correct text is diagonal:

```
Loss_img = CE(S / temperature, target = [0,1,2,...])
```

#### (2) Text → Image

```
Loss_txt = CE(S^T / temperature, target = [0,1,2,...])
```

Final loss:

```
Loss = (Loss_img + Loss_txt) / 2
```

---

## 3. Temperature parameter

CLIP uses a learnable scaling factor:

```
logits = S * exp(t)
```

This controls sharpness of similarity distribution.

---

## 4. Data you need

You need **millions to billions of (image, text) pairs**:

Common datasets:

* LAION-400M / LAION-5B
* Conceptual Captions (CC3M / CC12M)
* Web scraped alt-text data

Important:

> Data quality matters more than model size.

---

## 5. Model architecture (standard setup)

### Image encoder

* ViT-B/32 (fast baseline)
* ViT-L/14 (strong performance)

### Text encoder

* Transformer (similar to GPT encoder stack)
* Max length usually 77 tokens (CLIP standard)

---

## 6. Training pipeline

### Step 1: Preprocess data

Each sample:

```
(image, text caption)
```

Normalize images, tokenize text.

---

### Step 2: Forward pass

```python
img_emb = image_encoder(image)      # [B, d]
txt_emb = text_encoder(text)        # [B, d]
```

Normalize:

```python
img_emb = img_emb / ||img_emb||
txt_emb = txt_emb / ||txt_emb||
```

---

### Step 3: similarity matrix

```python
logits = img_emb @ txt_emb.T
logits *= exp(logit_scale)
```

---

### Step 4: compute loss

```python
labels = torch.arange(batch_size)

loss_i = cross_entropy(logits, labels)
loss_t = cross_entropy(logits.T, labels)

loss = (loss_i + loss_t) / 2
```

---

## 7. Minimal PyTorch-style code

```python id="clip_train_min"
import torch
import torch.nn.functional as F

def clip_loss(image_features, text_features, logit_scale):
    # normalize
    image_features = F.normalize(image_features, dim=-1)
    text_features  = F.normalize(text_features, dim=-1)

    # similarity matrix
    logits = logit_scale * image_features @ text_features.T

    labels = torch.arange(logits.size(0), device=logits.device)

    loss_i = F.cross_entropy(logits, labels)
    loss_t = F.cross_entropy(logits.T, labels)

    return (loss_i + loss_t) / 2
```

---

## 8. Training tips (very important)

### (1) Large batch size matters

CLIP relies heavily on negatives:

* 256 → weak
* 4096+ → good
* 32k → state-of-the-art

Use:

* gradient accumulation
* distributed training (DDP / FSDP)

---

### (2) Hard negatives improve quality

Random negatives are easy → weak learning.

Better:

* nearest neighbor negatives
* same-category images

---

### (3) Use strong image encoder

ViT-L/14 is a sweet spot.

---

### (4) Mixed precision

Use FP16 / BF16 for speed.

---

## 9. Why CLIP works so well

Because it learns:

* semantic alignment (not pixel-level)
* general visual concepts
* open-vocabulary retrieval

That’s why modern systems use it for:

* image search
* multimodal LLM grounding
* RAG over images

---

## 10. If you want next step

I can show you:

* how to train CLIP on **RTX 4070 (small-scale version)**
* how to extend CLIP into **SigLIP / modern contrastive loss**
* or how CLIP becomes the **vision front-end of LLaVA / GPT-4V style models**