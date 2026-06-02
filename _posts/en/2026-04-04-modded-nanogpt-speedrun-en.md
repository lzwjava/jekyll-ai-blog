---
audio: false
generated: true
image: false
lang: en
layout: post
title: Modded NanoGPT Speedrun Benchmark
translated: false
type: note
---

Question: Comprehensive introduction to the modded-nanogpt project

Answer:

**modded-nanogpt** is an open-source GitHub repository that serves as a high-performance "speedrun" benchmark for training a small GPT-style language model. It focuses on achieving a specific performance target—**3.28 cross-entropy validation loss** on the first 10,485,760 tokens of the **FineWeb** dataset—as quickly as possible using **8 NVIDIA H100 GPUs**.

### Origins and Lineage

The project builds directly on Andrej Karpathy's educational work:

- It descends from **nanoGPT**, Karpathy's minimalist PyTorch implementation of GPT-2 (~124M parameters).
- It uses the PyTorch GPT-2 trainer from Karpathy's **llm.c** repository as its starting point.
- The original llm.c GPT-2 replication took roughly **45 minutes** on 8xH100 to reach the target loss. Through community-driven optimizations in modded-nanogpt, this has been reduced dramatically—to around **2 minutes** (with records as low as ~2:20 in some reports).

The name "modded-nanogpt" reflects its evolution: heavy modifications ("modded") to the original nanoGPT baseline for extreme wall-clock speed on modern hardware. It is maintained primarily by Keller Jordan, with contributions from a collaborative/competitive community.

### Core Objective: The NanoGPT Speedrun

This is not a general-purpose training framework but a **speedrunning challenge**:

- **Goal**: Train a ~124M parameter model to 3.28 val loss on FineWeb (a large web-derived dataset) in minimal time on exactly 8xH100 GPUs.
- **Rules/Setup**: The code includes a full end-to-end pipeline (data loading, tokenizer handling, training, evaluation). A `speedrun.sh` script (or Docker build) reproduces the current record.
- **Leaderboard**: The repo tracks world records over time, showing progressive improvements from minutes down to ~2 minutes.

It emphasizes **wall-clock time** over other metrics like data efficiency or generalization, though many optimizations incidentally improve efficiency.

### Key Innovations and Optimizations

The dramatic speed gains come from a combination of architectural, algorithmic, systems, and numerical improvements. Notable techniques include:

- **Architecture Changes**:
  - Rotary Positional Embeddings (RoPE).
  - QK-Norm (Query-Key normalization).
  - ReLU² activation in the MLP.
  - Value embeddings mixed into attention layers.
  - Skip connections (e.g., from embeddings to every block, or specific block-to-block skips).
  - Flex Attention, short-long attention windows, attention window warmup.
  - Custom FP8 (8-bit floating point) operations, especially for the language modeling head, with asymmetric rescaling and softcapping of logits.

- **Optimizer**:
  - **Muon** optimizer (developed by Keller Jordan) for linear layers, which often outperforms tuned AdamW in this regime. Many forks experiment with alternatives like SOAP.

- **Training Techniques**:
  - muP-like initialization (projections initialized to zero).
  - Document alignment for better data packing.
  - Linear learning rate cooldown.
  - Reduce-scatter for gradient updates.
  - Parameter banks and other memory/throughput tricks.

- **Systems-Level Optimizations**:
  - Heavy use of custom Triton kernels for GPU efficiency.
  - Compiler configurations, torch.compile integrations, and low-level CUDA/FP8 tweaks.
  - Parallelism strategies tailored to 8xH100 (e.g., data parallelism with optimized communication).

These changes are aggressively tuned for the specific hardware and target. Not all generalize perfectly to larger models or different setups, but many have influenced downstream projects.

### How to Run It

The repo provides straightforward reproduction:

1. Clone the repository: `git clone https://github.com/KellerJordan/modded-nanogpt.git`
2. Build and run via Docker for the current record: `sudo docker build -t modded-nanogpt .` followed by running the container.
3. Or execute scripts directly (e.g., `speedrun.sh` or `train_gpt.py`).

It includes Wandb logging, benchmarking, and generation capabilities in related discussions.

### Impact and Community Influence

- **Research Harness**: Beyond speedrunning, it acts as a testbed for experimenting with new optimizers, architectures, and kernels at small scale. Innovations from modded-nanogpt have been "downstreamed" into other projects.
- **nanochat**: A related project inspired by modded-nanogpt, incorporating scaling laws, RL elements, and chatbot-focused features. Some modded optimizations have flowed into it.
- **Forks and Variants**: Numerous forks exist for different hardware (e.g., JAX/TPU ports), optimizers (e.g., SOAP), or baselines (e.g., RWKV experiments, "remixed" versions for stronger vanilla comparisons). Examples include modded-nanogpt-rwkv, modded-nanogpt-SOAP, and modded-nanogpt-jax.
- **Broader Lessons**: It demonstrates how much performance can be squeezed from a transformer through careful engineering. It has sparked discussions on data efficiency, scaling laws, and even recursive self-improvement benchmarks. Karpathy himself has praised it as an evolution of nanoGPT into a small-scale LLM research tool.

### Educational Value

While optimized for speed rather than readability, the core `train_gpt.py` (and related files like Triton kernels) offers deep insights into modern LLM training. Walkthroughs exist online covering setup, FP8 ops, parallelism, attention mechanisms, and the optimizer. It is more complex than original nanoGPT but remains far more accessible than production frameworks like Hugging Face Transformers.

In summary, modded-nanogpt transforms a simple educational GPT trainer into a cutting-edge optimization playground. It highlights the rapid progress possible in LLM training through open collaboration and low-level engineering, turning what was once a 45-minute task into a sub-3-minute feat on high-end hardware.

References:

- [https://github.com/KellerJordan/modded-nanogpt](https://github.com/KellerJordan/modded-nanogpt)
- [https://www.lesswrong.com/posts/j3gp8tebQiFJqzBgg/how-the-nanogpt-speedrun-wr-dropped-by-20-in-3-months](https://www.lesswrong.com/posts/j3gp8tebQiFJqzBgg/how-the-nanogpt-speedrun-wr-dropped-by-20-in-3-months)
- [https://damek.github.io/random/modded-nanogpt-walkthrough-i/](https://damek.github.io/random/modded-nanogpt-walkthrough-i/)
- [https://github.com/karpathy/llm.c](https://github.com/karpathy/llm.c) (for original baseline context)
- [https://kellerjordan.github.io/posts/muon/](https://kellerjordan.github.io/posts/muon/) (Muon optimizer writeup)
