---
audio: false
generated: true
image: false
lang: en
layout: post
title: 2GB VRAM AI Experiments Guide
translated: false
type: note
---

**Question:** With a 2 GB VRAM GPU, what LLM and AI experiments are feasible?

**Answer:**

Yes — 2 GB VRAM is tight, but you can still do meaningful experiments. Here's what's realistic:

---

### ✅ What You CAN Do

**1. Small / Quantized LLMs (Inference)**
- **Phi-2, Phi-3 Mini** (Microsoft) — very capable small models, runnable with 4-bit quantization (GGUF format via `llama.cpp`)
- **TinyLlama 1.1B** — designed to run on minimal hardware
- **Qwen 0.5B / 1.5B** — lightweight multilingual models
- **Gemma 2B** (quantized) — may fit at Q4 quantization
- Use **llama.cpp** or **Ollama** — these offload layers to CPU when VRAM is full

**2. Embedding Models**
- `sentence-transformers` (e.g., `all-MiniLM-L6-v2`) — runs almost entirely on CPU, VRAM not a bottleneck
- Great for RAG (Retrieval-Augmented Generation) pipelines

**3. Vision / Multimodal (Small)**
- **CLIP** (image-text embeddings) — very VRAM-efficient
- **ViT-tiny / ViT-small** for image classification

**4. Classic ML / Deep Learning**
- CNNs, RNNs, small Transformers trained from scratch — 2 GB is enough for small batch sizes
- `scikit-learn`, `XGBoost`, `LightGBM` — CPU-based, no VRAM needed at all

**5. Fine-tuning (with care)**
- **LoRA / QLoRA** on tiny models (e.g., GPT-2, DistilBERT) — possible with gradient checkpointing and small batch sizes

---

### ❌ What Will Struggle

- Running 7B+ models at full precision (need ~14 GB+)
- Fine-tuning large models even with LoRA (needs 6–8 GB minimum comfortably)
- Stable Diffusion (needs ~4–6 GB VRAM for SD 1.5)

---

### 🛠 Recommended Stack

| Tool | Purpose |
|------|---------|
| `llama.cpp` / `Ollama` | Run quantized LLMs locally |
| `Hugging Face Transformers` | Experiment with BERT, GPT-2, etc. |
| `sentence-transformers` | Embeddings & semantic search |
| `LangChain` / `LlamaIndex` | Build RAG apps |
| `PyTorch` | Custom model training |

---

### 💡 Pro Tip
Combine your 2 GB GPU with **CPU offloading** in `llama.cpp`. A model like TinyLlama or Phi-3-mini can split layers between GPU and RAM — you get GPU acceleration without needing everything to fit in VRAM.

---

**References:**
- [llama.cpp - Run LLMs locally](https://github.com/ggerganov/llama.cpp)
- [Ollama - Run models locally](https://ollama.com)
- [TinyLlama Model](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)
- [Microsoft Phi-3 Mini](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct)
- [Sentence Transformers](https://www.sbert.net/)
- [Hugging Face - Quantization Guide](https://huggingface.co/docs/transformers/main/en/quantization/overview)
