---
audio: false
generated: true
image: false
lang: en
layout: post
title: SM120 Blackwell Ultra Inference Optimization
translated: false
type: note
---

**Question:** What does "SM120" mean in the context of "Inference Optimization with AI Agents in the Workflow"?

**Answer:**

**SM120** refers to **NVIDIA's SM (Streaming Multiprocessor) generation 120** — this is the compute architecture generation identifier used internally in CUDA/PTX.

Specifically, SM120 corresponds to **Blackwell** architecture (GB200/B200/B100 GPUs), announced in 2024 and shipping in 2025.

The SM numbering follows NVIDIA's architecture generations:

| SM version | Architecture | GPUs |
|---|---|---|
| SM80 | Ampere | A100, A10 |
| SM86 | Ampere | RTX 3090 |
| SM89 | Ada Lovelace | RTX 4090 |
| SM90 | Hopper | H100, H200 |
| SM100 | Blackwell (first gen) | B100, B200 |
| **SM120** | **Blackwell Ultra** | **GB300, B300** |

So "SM120 Inference Optimization with AI Agents in the Workflow" is likely a **talk or paper title from GTC 2025 or similar NVIDIA event**, specifically about optimizing LLM inference on **Blackwell Ultra** GPUs using agentic workflows.

In CUDA terms, you'd target this with:

```bash
nvcc --gpu-architecture=sm_120 ...
```

or in PyTorch:

```python
torch.cuda.get_device_capability()  # returns (12, 0) for SM120
```

Do you have a link to the specific talk/paper? I can dig into the actual content if so.
