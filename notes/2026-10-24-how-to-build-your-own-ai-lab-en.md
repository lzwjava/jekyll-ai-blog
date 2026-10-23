---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Build Your Own AI Lab
translated: false
type: note
---

**Question:** Is it possible or doable for me to run a lab like the one at <https://truth-lab.lzwjava.workers.dev>?

**Answer:**

Yes — absolutely doable. The site is Zhiwei Li's personal one-person AI research lab, and every component he uses is open-source or available secondhand. Here's a realistic breakdown:

---

### 1. The Website Itself (very easy)

The site is hosted on Cloudflare Workers (`*.workers.dev`) — meaning it's a static page served via Cloudflare's free edge network. You can clone his approach with:

- A free Cloudflare Workers account
- A single HTML/CSS file (no backend needed)
- Zero cost to host

---

### 2. The GPU Hardware (moderate cost, moderate effort)

He built a 52 GB CUDA VRAM cluster from three second-hand datacenter workstations — Tesla M40 12 GB, M40 24 GB, and P100 16 GB — for roughly 100 CNY per GB of VRAM. That's about $140 for 12 GB. The catch: making it work required BIOS archaeology — specifically enabling Above 4G Decoding, disabling CSM, and putting the M40 in the CPU-attached x16 PCIe slot on an MSI Z170A Gaming M5 board.

For a simpler start, a **single RTX 4070 (12 GB, ~$400–600 new)** gets you very far. He ran most of his training runs on exactly that.

---

### 3. Training Small LLMs (learnable, weeks to months)

He pretrained GPT-2 at 124M and 760M parameters from zero on FineWeb, OpenWebText, and SEC filings — not from a checkpoint. The tooling is all open-source:

- **nanoGPT** (Karpathy's repo, his 45-commit fork is public)
- **PyTorch** + standard Python stack
- Public datasets (FineWeb, OpenWebText, Wikipedia dumps)

The SEC-EDGAR-GPT model took about 8 hours on a single RTX 4070 and the whole pipeline — training, paper, chatbot, website — was done in three days with an AI coding agent.

---

### 4. Inference Serving (moderate)

He runs vLLM, SGLang (compiled from source), and llama.cpp to serve open models like Qwen3-0.6B and DeepSeek-R1-14B GGUF locally. All free and well-documented. The main hurdle is CUDA environment setup, especially for older GPU architectures like the M40 (Maxwell, CC 5.2).

---

### 5. What You Actually Need

| Component | Minimum to start | Cost |
| --- | --- | --- |
| Website | Cloudflare Workers (free) | $0 |
| GPU | RTX 4070 12 GB (or rent RunPod/Lambda) | $400–600 or ~$1–3/hr |
| Training | nanoGPT + PyTorch + public datasets | $0 software |
| Serving | llama.cpp or vLLM | $0 software |
| Skills | Python, Linux, basic ML concepts | Time |

---

### Bottom Line

The **website** takes an afternoon. The **lab** (actual GPU work) is genuinely doable in months if you have some engineering background — he did it alongside a day job. His honest lesson: verify code, environment, and data before spending GPU hours — a broken pipeline always fails during training. Cloud GPUs (RunPod, Lambda) let you skip the hardware entirely to start.

**References:**

- [Truth Lab — Zhiwei Li](https://truth-lab.lzwjava.workers.dev)
- [lzwjava/nanoGPT (GitHub)](https://github.com/lzwjava/nanoGPT)
- [lzwjava/sec-edgar-gpt (GitHub)](https://github.com/lzwjava/sec-edgar-gpt)
