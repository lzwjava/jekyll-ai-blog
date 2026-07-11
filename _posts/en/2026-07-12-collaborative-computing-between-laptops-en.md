---
audio: false
generated: true
image: false
lang: en
layout: post
title: Collaborative Computing Between Laptops
translated: false
type: note
---

Question: How can two laptops or computers collaborate to do tasks together?

Answer:

There are several levels of collaboration, from simple file sharing to distributed computing.

## 1. Remote control (one computer controls another)

The simplest model:

```
Laptop A  --->  Laptop B
          SSH / Remote Desktop
```

Examples:

### SSH (Linux/macOS/Windows)

Laptop A:

```bash
ssh user@laptop-b-ip
```

Then you can run commands on B:

```bash
python train.py
```

The computation happens on B.

For AI development this is common:

```
Your laptop
    |
    | ssh
    v
GPU workstation
    |
    v
training / inference
```

---

## 2. Share files and code

Use Git:

```
Computer A
   |
   | git push
   v
GitHub/GitLab
   |
   | git pull
   v
Computer B
```

Example:

Computer A:

```bash
git add .
git commit -m "experiment"
git push
```

Computer B:

```bash
git pull
```

Both machines have the same code.

---

## 3. Split a workload (distributed computing)

For AI training:

```
              PyTorch Distributed

        +----------------+
        |  Master node   |
        |   Laptop A    |
        +----------------+
              |
       network (NCCL/Gloo)
              |
        +----------------+
        | Worker node    |
        |   Laptop B    |
        +----------------+
```

Example:

Two GPUs:

```
GPU0 -> Computer A
GPU1 -> Computer B
```

PyTorch:

```python
torch.distributed.init_process_group(
    backend="nccl"
)
```

Run:

Computer A:

```bash
torchrun \
 --nproc_per_node=1 \
 --nnodes=2 \
 --node_rank=0 \
 train.py
```

Computer B:

```bash
torchrun \
 --nproc_per_node=1 \
 --nnodes=2 \
 --node_rank=1 \
 train.py
```

The model training is synchronized.

---

## 4. Use one as a server

Very common for engineers:

```
Laptop
   |
   | API request
   |
   v
Desktop with GPU

RTX 4070 / MI50 / H100
```

Example:

Computer B:

```bash
vllm serve qwen-model
```

Computer A:

```python
requests.post(
 "http://computer-b:8000/v1/chat/completions"
)
```

Your laptop becomes the "terminal"; GPU machine does the heavy work.

---

## 5. Kubernetes / cluster style

More advanced:

```
             Kubernetes Cluster

       +----------------+
       | Control Plane  |
       | Computer A    |
       +----------------+

          |
    ----------------
    |              |
Computer B     Computer C
 GPU worker    GPU worker
```

Jobs are scheduled automatically.

---

## 6. Shared folder

Simple home lab:

```
Computer A
      \
       \
      NAS / Shared Storage
       /
      /
Computer B
```

Using:

* NFS
* SMB
* Syncthing
* MinIO

Example:

```bash
mount server:/data /mnt/data
```

Both computers see the same files.

---

For your AI workstation situation (RTX 4070 + possible AMD MI50), a practical setup would be:

```
                 Network

MacBook/Laptop
      |
      | SSH
      |
      v
AI Desktop
      |
      |
 RTX 4070
 MI50
```

Laptop:

* write code
* monitor training
* browse logs

Desktop:

* GPU training
* model inference
* dataset processing

Then later:

```
Machine A RTX 4070
        +
Machine B MI50
        +
Machine C cloud GPU

        |
        v

Distributed PyTorch training
```

This is basically how small AI labs grow: start with 2 machines, then turn them into a mini cluster.
