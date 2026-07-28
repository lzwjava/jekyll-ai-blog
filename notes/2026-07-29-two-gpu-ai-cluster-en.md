---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two-GPU AI Cluster
translated: false
type: note
---

Question: How should two separate AI workstations (RTX 4070 + RTX 3060/3090) be used together?

Answer:

With **two separate machines**, you should think of them as a small **AI cluster**, not as one computer.

Example:

```
                LAN (1GbE/10GbE)
                     |
        ----------------------------
        |                          |
 Workstation A              Workstation B
 RTX 4070 12GB              RTX 3090 24GB
 Ubuntu                     Ubuntu
 PyTorch                    vLLM
 Training                   Inference
```

The best use depends on the GPU combination.

---

## Case 1: RTX 4070 + RTX 3090 (best combination)

This is actually a very nice home lab.

### Machine A: RTX 4070

Role:

* fast experiments
* fine-tuning
* code development
* smaller models

Examples:

```
GPT-2 124M
GPT-2 355M
Qwen3-8B LoRA
embedding models
agent experiments
```

### Machine B: RTX 3090 24GB

Role:

* large inference
* bigger fine-tuning
* evaluation server

Examples:

```
Qwen3-8B
Llama 8B
DeepSeek distilled models
FLUX image models
```

Because 3090 has:

```
24GB VRAM
vs
4070 12GB VRAM
```

the 3090 unlocks a different class of models.

---

## Recommended workflow

Think like an AI research team:

```
                 Git repo
                    |
        ------------------------
        |                      |
 RTX 4070 machine       RTX 3090 machine
        |                      |
 experiment             evaluation
 training               serving
        |                      |
 checkpoint  ----------->  test
```

Example:

You train:

```
GPU0:
python train.py \
 --model gpt2-124m \
 --lr 3e-4
```

It produces:

```
checkpoint_10000.pt
```

3090 automatically evaluates:

```
python eval.py \
 checkpoint_10000.pt
```

---

## Use SSH + shared storage

The simplest cluster setup:

Machine names:

```
ai4070
ai3090
```

SSH:

```bash
ssh ai3090
```

Shared directory:

Option 1:

NFS:

```
ai4070:/data

mounted on:

ai3090:/data
```

Option 2:

Git + rsync:

```bash
rsync -av checkpoints/ ai3090:/data/checkpoints/
```

---

## Run experiments remotely

Example:

On 4070:

```bash
ssh ai3090 \
"CUDA_VISIBLE_DEVICES=0 \
python eval.py \
--checkpoint /data/model.pt"
```

Your laptop becomes the controller.

---

## Add a lightweight scheduler

Install Ray on both:

```
pip install ray
```

Head node:

3090:

```bash
ray start --head
```

Output:

```
ray://192.168.1.100:10001
```

Worker:

4070:

```bash
ray start \
--address='192.168.1.100:6379'
```

Now:

```
Ray cluster

GPU resources:

node1:
 RTX3090: 1 GPU

node2:
 RTX4070: 1 GPU
```

Your experiments request:

```python
@ray.remote(num_gpus=1)
class Experiment:
    pass
```

Ray decides where to run.

---

## What I would NOT do

Avoid:

```
RTX4070 + RTX3090
       |
       |
    Distributed training
```

unless you have a reason.

Why?

Different GPUs:

```
4070:
Ada Lovelace
12GB

3090:
Ampere
24GB
```

Problems:

* different CUDA performance
* different VRAM
* PCIe network bottleneck
* synchronization overhead

For LLM training, two independent jobs are usually better.

---

## A practical setup for your experiments

Given your previous GPT-2/nanoGPT work:

### RTX 4070 box

```
Role:
research workstation

run:
- nanoGPT training
- data preprocessing
- small LoRA
- coding agents
```

### RTX 3090 box

```
Role:
AI server

run:
- vLLM
- Ollama
- Qwen models
- embedding service
- evaluation
```

Then you have:

```
          Claude/Gemini
               |
               |
          AI Agent CLI
               |
       -----------------
       |               |
   RTX4070          RTX3090
   create           execute
   train            serve
```

This is close to a tiny version of an internal AI lab.

---

For home use, I would choose:

1. **RTX 3090 24GB as the main AI server**
2. **RTX 4070 as the daily development/training machine**
3. Connect with **10GbE if possible** (especially for datasets/checkpoints)
4. Add Ray only after SSH + shared storage becomes annoying

That gives much more practical throughput than trying to make them one giant GPU.
