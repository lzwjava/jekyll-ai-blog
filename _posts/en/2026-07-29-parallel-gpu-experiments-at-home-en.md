---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parallel GPU Experiments at Home
translated: false
type: note
---

Question: Suppose we have two GPUs in a local home lab. How can we use them to run more parallel experiments?

Answer:

For a home AI lab, **do not immediately think "combine two GPUs into one big GPU"**. The highest ROI is usually **parallel experiment scheduling**:

```
GPU0  -> experiment A
GPU1  -> experiment B

or

GPU0  -> training
GPU1  -> evaluation / inference / data processing
```

This gives almost 2x productivity because ML research is usually many trials, not one giant run.

## 1. Simplest: manual GPU assignment

Example:

Machine:

```
CPU
 |
 +-- RTX 4070 12GB (GPU0)
 |
 +-- RTX 3090 24GB (GPU1)
```

Run:

Terminal 1:

```bash
CUDA_VISIBLE_DEVICES=0 python train.py \
  --lr 3e-4 \
  --batch-size 32 \
  --exp exp_lr3e4
```

Terminal 2:

```bash
CUDA_VISIBLE_DEVICES=1 python train.py \
  --lr 1e-4 \
  --batch-size 64 \
  --exp exp_lr1e4
```

You are doing hyperparameter search.

Instead of:

```
one experiment = 8 hours
```

you get:

```
experiment A = 8 hours
experiment B = 8 hours

total research throughput = 2x
```

---

## 2. Use a job scheduler (mini Kubernetes style)

For a serious home lab, create a GPU queue.

Example:

```
~/gpu-cluster

jobs/
 ├── train_gpt2_124m.yaml
 ├── finetune_qwen.yaml
 └── eval.yaml
```

A simple Python scheduler:

```python
import subprocess
import time

jobs = [
    {
        "gpu":0,
        "cmd":"python train.py --model gpt2-small"
    },
    {
        "gpu":1,
        "cmd":"python train.py --model qwen"
    }
]


for job in jobs:
    env = {
        "CUDA_VISIBLE_DEVICES":str(job["gpu"])
    }

    subprocess.Popen(
        job["cmd"],
        shell=True,
        env=env
    )
```

Basically your own tiny Slurm.

---

## 3. Distributed training (two GPUs = one bigger GPU)

Sometimes you need this:

```
        model
          |
 ----------------
 |              |
GPU0           GPU1
```

PyTorch DDP:

```bash
torchrun \
 --nproc_per_node=2 \
 train.py
```

Inside:

```python
model = MyModel()

model = torch.nn.parallel.DistributedDataParallel(
    model,
    device_ids=[local_rank]
)
```

Now:

```
GPU0:
layers + gradients

GPU1:
layers + gradients
```

Effective VRAM:

Not exactly:

```
12GB + 12GB = 24GB
```

because each GPU usually stores a copy of parameters.

For example:

```
model weights:
10GB

GPU0:
10GB weights
+
GPU1:
10GB weights
```

So DDP gives speed, not memory expansion.

---

## 4. Better for LLM experiments: split roles

For your kind of workflow (GPT-2 training, Qwen testing, agents), I would do:

```
GPU0: training

GPU1: inference + evaluation
```

Example:

```
RTX 4070
 |
 +-- train GPT-2 124M


RTX 3090
 |
 +-- vLLM
 +-- embedding
 +-- dataset filtering
 +-- eval harness
```

Then your loop becomes:

```
train
 |
checkpoint
 |
eval GPU1
 |
metrics
 |
change hyperparameters
 |
train again
```

This is much closer to how research teams operate.

---

## 5. Use containers

Install:

* Docker
* NVIDIA Container Toolkit

Then:

container A:

```bash
docker run \
 --gpus '"device=0"' \
 pytorch-training
```

container B:

```bash
docker run \
 --gpus '"device=1"' \
 vllm-server
```

You get isolation:

```
host
 |
 +-- training container GPU0
 |
 +-- inference container GPU1
```

---

## 6. For multiple experiments: use Ray

Ray is very nice for AI labs.

Install:

```bash
pip install ray
```

Example:

```python
import ray

ray.init()

@ray.remote(num_gpus=1)
class Trainer:
    def run(self):
        import torch
        print(torch.cuda.current_device())


a = Trainer.remote()
b = Trainer.remote()

ray.get([
    a.run.remote(),
    b.run.remote()
])
```

Ray automatically schedules:

```
job A -> GPU0
job B -> GPU1
```

This is the direction many AI agent systems are going.

---

## 7. A realistic home AI lab architecture

Given your experiments (nanoGPT, Qwen, agents), I would build:

```
             Home Server
                 |
        ---------------------
        |                   |
      GPU0                GPU1
   Training            Serving
        |                   |
   PyTorch             vLLM/Ollama
        |
   checkpoints
        |
      Eval
```

Software:

```
Ubuntu
 |
 +-- Docker
 |
 +-- NVIDIA Container Toolkit
 |
 +-- Ray
 |
 +-- MLflow/W&B
```

Then every experiment becomes:

```bash
submit experiment.yaml
```

Example:

```yaml
name: gpt2-small-lr-test

gpu: auto

train:
  model: 124m
  lr:
    - 1e-4
    - 3e-4
    - 1e-3
```

Scheduler launches:

```
GPU0:
lr=1e-4

GPU1:
lr=3e-4

later:
lr=1e-3
```

---

For a **2-GPU home lab**, I would rank approaches:

| Approach                    | Productivity |
| --------------------------- | -----------: |
| Two independent experiments |        ⭐⭐⭐⭐⭐ |
| Training + inference split  |        ⭐⭐⭐⭐⭐ |
| Ray scheduler               |         ⭐⭐⭐⭐ |
| Docker GPU isolation        |         ⭐⭐⭐⭐ |
| DDP training                |          ⭐⭐⭐ |
| Model parallelism           |           ⭐⭐ |

The biggest upgrade is not "more FLOPS"; it is turning your machine into a **small AI research cluster where experiments continuously run without you babysitting them**.
