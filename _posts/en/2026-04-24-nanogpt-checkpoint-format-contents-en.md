---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoGPT Checkpoint Format and Contents
translated: false
type: note
---

Question: What is the format of `ckpt.pt` in nanoGPT and what does it contain (e.g., model parameters)?

Answer:

In nanoGPT, a file like:

```
out-fineweb/ckpt.pt
```

is a **PyTorch checkpoint file** saved using `torch.save()`.

It is not a simple text or model-only file — it is a **Python serialized dictionary** that typically contains everything needed to resume training or run inference.

---

## 1. What format is `ckpt.pt`?

It is usually a **PyTorch Pickle-based binary file**, created like:

```python
torch.save(state, "ckpt.pt")
```

So internally it is a **serialized Python dict**, not a standardized model format like ONNX.

You cannot read it directly with `cat`; you must load it with PyTorch:

```python
import torch

ckpt = torch.load("ckpt.pt", map_location="cpu")
```

---

## 2. What does nanoGPT store inside `ckpt.pt`?

In nanoGPT (Andrej Karpathy’s implementation), a checkpoint typically contains a dictionary like:

### Core structure:

```python
{
    "model": model_state_dict,
    "optimizer": optimizer_state_dict,
    "model_args": {...},
    "iter_num": int,
    "best_val_loss": float,
    "config": {...},
}
```

---

## 3. Main components explained

### (1) Model parameters (weights)

```python
"model": model.state_dict()
```

This is the most important part:

* Embedding weights
* Transformer blocks

  * attention weights (Q, K, V projections)
  * MLP layers
* LayerNorm parameters
* Output head

👉 This is the **trained neural network parameters**

---

### (2) Optimizer state

```python
"optimizer": optimizer.state_dict()
```

Contains:

* Adam momentum buffers
* Second-order moments (m/v)
* learning rate scheduling state

👉 Needed only if you want to **resume training exactly**

---

### (3) Training metadata

```python
"iter_num": 12345
"best_val_loss": 2.31
```

Used for:

* resuming training step count
* tracking best checkpoint

---

### (4) Model configuration

```python
"model_args": {
    "n_layer": 12,
    "n_head": 12,
    "n_embd": 768,
    ...
}
```

Defines architecture so model can be rebuilt exactly.

---

## 4. What is NOT inside

A nanoGPT checkpoint usually does NOT contain:

* raw dataset
* tokenizer files (unless separately saved)
* training code
* logs

---

## 5. Is it just “params”?

Yes — but more precisely:

👉 It contains:

* **parameters (weights)**
* **optimizer state**
* **architecture config**
* **training progress metadata**

So it is a **full training snapshot**, not just a model.

---

## 6. Typical size

Depends on model size:

* small GPT: ~100MB
* medium: 500MB–2GB
* large: multi-GB

---

## 7. How it is used

### Resume training:

```bash
python train.py --init_from=resume
```

### Inference:

load only `"model"` weights into model and run generation.

---

## 8. Key intuition

Think of `ckpt.pt` as:

> “A frozen snapshot of the entire training system at one moment in time”

---

If you want, I can also show:

* how to inspect `ckpt.pt` contents directly
* how nanoGPT maps this into Transformer layers
* or how to convert it to HuggingFace format