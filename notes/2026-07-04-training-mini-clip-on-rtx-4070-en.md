---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Mini CLIP on RTX 4070
translated: false
type: note
---

Question: How can I train a CLIP model on a single RTX 4070 GPU in a small-scale practical setup?

Answer:

Training full CLIP (like OpenAI scale) is impossible on a single RTX 4070, but you *can absolutely train a mini-CLIP* that works well for learning, experiments, and even small retrieval tasks.

The key is: **reduce model size + reduce batch size + use gradient accumulation + use a small dataset subset**.

---

# 1. What you can realistically train on RTX 4070

Your constraints:

* VRAM: ~12GB
* Good for: ViT-B/32 or smaller + small batch training
* Not good for: LAION-5B full training

### Recommended “student CLIP” setup:

* Image encoder: **ViT-B/32 or ResNet-50**
* Text encoder: **small Transformer (6 layers or CLIP default)**
* Embedding dim: 256–512
* Batch size: 32–128 (via accumulation)

---

# 2. Dataset (VERY important)

Do NOT use full LAION.

Use one of:

### Good starter datasets:

* COCO Captions (118k images)
* Conceptual Captions 3M (filtered subset)
* Flickr30k
* Or your own scraped dataset (small but clean)

👉 Start with COCO first. It is enough to verify correctness.

---

# 3. System design (simple version)

```
image → ViT encoder → projection → normalized vector
text  → Transformer → projection → normalized vector

dot product similarity → contrastive loss
```

---

# 4. Memory-saving tricks (critical for 4070)

### (1) Mixed precision

Use BF16 or FP16:

```python
torch.cuda.amp.autocast()
```

---

### (2) Gradient accumulation

Simulate large batch:

```python
effective_batch = batch_size * accumulation_steps
```

Example:

* batch_size = 16
* accumulation = 8
  → effective batch = 128

---

### (3) Freeze parts of model (optional)

To start easier:

* freeze image encoder OR text encoder

Then later unfreeze.

---

### (4) Use smaller resolution

* CLIP default: 224×224
* You can even start at 128×128 for speed

---

# 5. Minimal training pipeline

## Step 1: Load encoders

```python
from transformers import CLIPModel, CLIPProcessor

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
```

---

## Step 2: Dataset format

Each sample:

```python
{
  "image": PIL.Image,
  "text": "a dog running in grass"
}
```

---

## Step 3: Forward pass

```python
outputs = model(
    input_ids=text_inputs,
    pixel_values=image_inputs
)

loss = outputs.loss
```

HuggingFace already implements CLIP loss internally.

---

# 6. Full training loop (practical version)

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for step, batch in enumerate(loader):

    images = batch["image"].to(device)
    texts  = batch["text_inputs"].to(device)

    with autocast():
        outputs = model(
            input_ids=texts,
            pixel_values=images,
            return_loss=True
        )
        loss = outputs.loss / accumulation_steps

    scaler.scale(loss).backward()

    if step % accumulation_steps == 0:
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

---

# 7. Recommended hyperparameters (RTX 4070)

| Parameter       | Value        |
| --------------- | ------------ |
| image encoder   | ViT-B/32     |
| batch size      | 8–16         |
| accumulation    | 8–16         |
| effective batch | 64–256       |
| learning rate   | 1e-5 to 5e-5 |
| optimizer       | AdamW        |
| precision       | FP16         |
| epochs          | 5–20         |

---

# 8. Expected training time

On RTX 4070:

### COCO dataset:

* ~1–3 hours per epoch
* full training: ~10–30 hours

### CC3M subset:

* ~1–3 days depending on filtering

---

# 9. Common mistakes

### ❌ Too large batch expectation

CLIP needs negatives, but you compensate with accumulation.

---

### ❌ No data cleaning

Bad captions = bad model

Fix:

* remove short captions (<3 words)
* remove noisy web text

---

### ❌ Not normalizing embeddings

Always:

```python
F.normalize(x, dim=-1)
```

---

# 10. How to know it works

After training, test:

### Text → image retrieval

Input:

> "a red car"

Model should retrieve red car images.

### Image → text

Input image:
→ should output correct caption match

---

# 11. Upgrade path after this

Once your mini-CLIP works:

You can upgrade to:

* ViT-L/14 CLIP
* SigLIP (better loss)
* BLIP-2 style Q-Former
* LLaVA vision encoder

---

If you want next step, I can show:

👉 how to build a **full LLaVA system on top of your CLIP**
👉 or how to train **CLIP faster with FAISS hard negatives**
👉 or how to scale from 4070 → multi-GPU training properly