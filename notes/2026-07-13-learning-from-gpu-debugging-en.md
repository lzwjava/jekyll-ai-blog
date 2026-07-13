---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning from GPU Debugging
translated: false
type: note
---

Question: Analyze this conversation and give a deeper reflection on the situation, especially the learning value and next AI research direction.

Answer:

Your friend is asking a simple operational question:

> "好了？修好了吗？"

But your answer is actually about something deeper: **the process of building capability**.

The MI50 itself is not the most valuable thing you got. The valuable part is the whole chain:

```
购买二手 GPU
      ↓
遇到硬件问题
      ↓
找维修店学习硬件诊断
      ↓
理解主板、电源、PCIe、GPU
      ↓
和不同的人交流经验
      ↓
用 AI 辅助学习
      ↓
重新思考自己的 AI 路线
```

This is very close to how many great engineers grow: not by following a perfect roadmap, but by repeatedly entering unknown systems and debugging them.

For example:

* Linus Torvalds did not start Linux because he knew the entire operating system field. He started by playing with hardware and writing code.
* Karpathy often emphasizes "understanding by building": implement the smallest version, observe failure modes, iterate.
* Many AI infrastructure engineers became strong because they had to debug CUDA, drivers, distributed systems, memory problems, not because they only read papers.

Your MI50 accident actually forced you to learn a missing layer:

Before:

```
AI model
   ↑
PyTorch
   ↑
CUDA/ROCm
   ↑
GPU
   ↑
PCIe / motherboard / power supply
```

After this event, you understand more of the bottom layers.

That matters because future AI engineers increasingly need the full stack:

```
Algorithm
   |
Model architecture
   |
Training system
   |
Compiler
   |
Kernel
   |
GPU runtime
   |
Hardware
```

Your current position is interesting:

You already have:

* software engineering background
* backend/distributed systems experience
* LLM training experiments
* GPT-2 from scratch experience
* GPU debugging experience

The next step should probably not be "buy more GPUs".

The better question:

**What unique advantage can one person create with cheap hardware?**

I would consider these directions:

### 1. Small-scale LLM research infrastructure

Your RTX 4070 + MI50 + cheap machines are enough.

Examples:

* implement distributed training from scratch

```
machine A
 RTX4070
   |
 NCCL / Gloo
   |
machine B
 MI50
```

Study:

* data parallelism
* tensor parallelism
* pipeline parallelism
* optimizer sharding

This directly connects to large-scale AI companies.

---

### 2. Efficient training research

This fits your hardware.

Instead of:

"train a bigger model"

try:

"train the best model under constraints"

Research:

* LoRA
* QLoRA
* knowledge distillation
* pruning
* quantization
* mixture of experts

The question:

> How can one person train useful models with $100 of compute?

is very valuable.

---

### 3. AI agent + engineering tools

Your background is unusually suitable.

You have:

* backend
* DevOps
* coding agents
* LLM knowledge

Potential project:

```
AI engineer agent

Input:
"I have a Linux kernel boot problem"

Agent:
- read logs
- inspect hardware
- search docs
- generate commands
- verify fixes
```

The MI50 repair experience itself is a dataset:

```
real-world debugging trajectory
        |
        |
AI troubleshooting agent
```

---

### 4. GPU / systems engineering

Your MI50 gives you a rare opportunity.

Many AI engineers only know:

```python
model = AutoModel.from_pretrained(...)
```

They don't know:

* PCIe topology
* VRAM failures
* driver stack
* firmware
* kernel modules
* ROCm

A person who understands:

```
PyTorch
 ↓
ROCm/CUDA
 ↓
Linux kernel
 ↓
GPU hardware
```

is rare.

---

The current situation is actually a good forced "research retreat":

7-15 days without the MI50 means:

Do not rush buying hardware.

Use this time:

```
Week 1:

Read:
- nanoGPT
- Megatron-LM
- DeepSpeed ZeRO papers

Implement:
- tiny distributed training

Experiment:
- 64M GPT model

Write:
- engineering notes
```

Your advantage is not owning 8 GPUs.

Your advantage is becoming someone who can connect:

```
hardware
+
systems
+
models
+
agents
+
products
```

A solo founder in AI probably wins from this intersection.

The Japanese concept you mentioned, ikigai, maps well here:

```
What you love:
AI + building

What you are good at:
engineering + systems

What society needs:
AI tools

What can make money:
AI consulting/products/jobs
```

The unknown future is unavoidable. But this kind of exploration is accumulating "optionality": every broken machine, failed experiment, and debugging session increases the number of things you can build.

The MI50 may have arrived by accident, but the learning path it created is not accidental.
