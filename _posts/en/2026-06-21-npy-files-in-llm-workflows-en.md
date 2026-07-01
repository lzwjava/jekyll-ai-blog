---
audio: false
generated: true
image: false
lang: en
layout: post
title: NPY Files in LLM Workflows
translated: false
type: note
---

**Question:** What are `.npy` files and how are they used in LLM workflows?

**Answer:**

`.npy` is NumPy's native binary serialization format. It stores a single ndarray — dtype, shape, and raw data — in a compact, memory-mappable file.

**Format internals:**

```
magic: \x93NUMPY          (6 bytes)
version: 1.0 or 2.0      (2 bytes)
header_len                (2 or 4 bytes)
header: dict with shape, dtype, fortran_order  (ASCII)
data: raw C-contiguous bytes
```

No compression, no overhead. Loading is essentially a `mmap` call.

---

**Where they show up in LLM pipelines:**

**1. Tokenized dataset storage (most common)**

After running a tokenizer over raw text, you dump token IDs as `uint16` or `uint32` arrays:

```python
import numpy as np

# nanoGPT style — train.bin / val.bin are actually raw uint16
ids = np.array(tokenized_ids, dtype=np.uint16)
ids.tofile("train.bin")  # raw binary, not .npy but same idea

# .npy version preserves shape/dtype metadata
np.save("train.npy", ids)
```

nanoGPT uses `.bin` (rawer), but many pipelines use `.npy` for the same purpose. Fineweb, RedPajama preprocessing scripts save shards as `.npy`.

**2. Memory-mapped training data**

The killer feature: `np.load(..., mmap_mode='r')` lets you index into a 200GB dataset without loading it all into RAM:

```python
data = np.load("train.npy", mmap_mode='r')
batch = data[offset : offset + block_size]  # OS pages in only what's needed
```

This is how you train on your RTX 4070 / MI300X with datasets larger than RAM.

**3. Embeddings cache**

Pre-computed embeddings saved for retrieval or fine-tuning:

```python
np.save("embeddings.npy", model.encode(texts))  # shape: (N, D)
# later:
embs = np.load("embeddings.npy")
```

**4. Checkpoint shards (less common now)**

Before safetensors became standard, people saved weight tensors as `.npy` or `.npz` (zipped multi-array). Still seen in older Hugging Face code.

**5. Activation / attention dumps for interpretability**

```python
# hook into a layer, save activations for analysis
np.save(f"layer_{i}_attn.npy", attn_weights.cpu().numpy())
```

---

**`.npy` vs alternatives:**

| Format | Use case | Notes |
| -------- | ---------- | ------- |
| `.npy` | single array | fast, mmap-able |
| `.npz` | multiple arrays | zipped, slower |
| `.bin` | raw bytes | nanoGPT style, no metadata |
| `.safetensors` | model weights | safe, fast, preferred now |
| `.pt` / `.ckpt` | PyTorch tensors | pickle-based, less safe |
| Arrow / Parquet | structured datasets | HF Datasets default |

---

**In your nanoGPT context specifically:**

`prepare.py` in nanoGPT does:

```python
train_ids = np.array(enc.encode_ordinary(train_data), dtype=np.uint16)
train_ids.tofile(os.path.join(os.path.dirname(__file__), 'train.bin'))
```

Raw `.bin` there, but the pattern is identical to `.npy` — dtype-homogeneous flat array of token IDs, mmap'd during training via:

```python
data = np.memmap('train.bin', dtype=np.uint16, mode='r')
```

Same principle, just skipping NumPy's header. `.npy` adds ~128 bytes of header in exchange for self-describing metadata.
