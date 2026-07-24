---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running Nano-vLLM Setup
translated: false
type: note
---

## How to Run Nano-vLLM

### 1️⃣ Prerequisites

Python 3.10–3.12 and CUDA-compatible GPU (or CPU-only with `enforce_eager=True`).

### 2️⃣ Install Dependencies

```bash
cd /mnt/data/nano-vllm

# Activate existing virtual env (if you want to use one of the ones already here)
source .venv/bin/activate    # or .venv311/bin/activate

# Or create a fresh one:
python3 -m venv .venv
source .venv/bin/activate

# Install the package in editable mode
pip install -e .
```

### 3️⃣ Download a Model

```bash
huggingface-cli download --resume-download Qwen/Qwen3-0.6B \
  --local-dir ~/huggingface/Qwen3-0.6B/ \
  --local-dir-use-symlinks False
```

### 4️⃣ Run the Example

```bash
# With GPU (default)
python example.py

# If no GPU / to avoid CUDA graph compilation:
# Edit example.py and ensure enforce_eager=True (already set)
python example.py
```

### 5️⃣ Run the Benchmark

```bash
python bench.py
```

---

### Quick One-Liner (if model already downloaded)

```bash
cd /mnt/data/nano-vllm && source .venv/bin/activate && python example.py
```

### Custom Inference

```python
from nanovllm import LLM, SamplingParams

llm = LLM("~/huggingface/Qwen3-0.6B/", enforce_eager=True)
params = SamplingParams(temperature=0.6, max_tokens=256)
outputs = llm.generate(["Hello, world!"], params)
print(outputs[0]["text"])
```