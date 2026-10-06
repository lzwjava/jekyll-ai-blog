---
audio: false
generated: true
image: false
lang: en
layout: post
title: Beyond Ubuntu for AI Workloads
translated: false
type: note
---

Question: Besides Ubuntu, what do people use to run models, PyTorch, and general LLM workloads?

Answer:

Ubuntu is the **dominant choice** for AI development, but it is not the only one. The ecosystem is mostly Linux-based because CUDA, drivers, distributed training, and cluster tools are built around Linux.

Common choices:

| OS                                 | Usage                             | Notes                                                    |
| ---------------------------------- | --------------------------------- | -------------------------------------------------------- |
| **Ubuntu Linux**                   | ⭐ Most common for AI research/dev | Best CUDA/PyTorch compatibility, easiest tutorials       |
| **Debian**                         | Servers, custom infrastructure    | More stable, slower package updates                      |
| **Rocky Linux / AlmaLinux / RHEL** | Enterprise AI clusters            | Common in universities and companies with HPC            |
| **CentOS (older)**                 | Legacy HPC clusters               | Being replaced by Rocky/Alma                             |
| **SUSE Linux Enterprise**          | Enterprise/HPC                    | Used in some supercomputing environments                 |
| **Arch Linux**                     | Individual developers             | Latest packages, more maintenance                        |
| **Fedora**                         | Developers                        | Newer Linux technologies                                 |
| **Windows + WSL2**                 | Local AI developers               | Very popular now; runs Ubuntu environment inside Windows |
| **macOS**                          | Development/testing               | Good for Apple Silicon, not CUDA training                |

---

## 1. Ubuntu (the default)

Most tutorials assume:

```
Ubuntu 22.04 / 24.04
CUDA
cuDNN
PyTorch
NVIDIA driver
```

Example:

```bash
sudo apt install nvidia-driver-580
pip install torch torchvision
python train.py
```

Most GitHub AI projects are tested on Ubuntu.

---

## 2. Windows + WSL2

A lot of individual developers use:

```
Windows
 └── WSL2
      └── Ubuntu
           ├── CUDA
           ├── PyTorch
           └── LLM tools
```

You get:

* Windows desktop/games/tools
* Linux AI environment

Example:

```powershell
wsl --install
```

Then inside Ubuntu:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

For a single RTX 4070/4090 workstation, this is very common.

---

## 3. Debian

Ubuntu itself is based on Debian.

Many servers use Debian:

```
Debian 12
 ├── NVIDIA driver
 ├── Docker
 ├── Kubernetes
 └── PyTorch containers
```

Advantages:

* Stable
* Minimal
* Good for long-running servers

Disadvantage:

* Some AI tutorials assume Ubuntu commands.

---

## 4. Enterprise Linux (Rocky / RHEL)

Large AI clusters often use:

```
Rocky Linux
      |
      +-- Slurm
      +-- CUDA
      +-- NCCL
      +-- PyTorch
```

Example environments:

* universities
* national labs
* cloud GPU clusters

They care about:

* 5-year support
* security patches
* predictable updates

---

## 5. Docker (actually more important than OS)

In modern AI, people often think:

```
Host OS
   |
   Docker
   |
   CUDA container
   |
   PyTorch
   |
   Model
```

Example:

```bash
docker run \
 --gpus all \
 -it \
 pytorch/pytorch:2.7.0-cuda12.8-cudnn9-runtime
```

This avoids "dependency hell".

A researcher may run:

```
Ubuntu 24.04 host

container:
    Ubuntu 22.04
    CUDA 12.6
    PyTorch 2.7
    Transformers
    FlashAttention
```

---

## 6. Cloud AI environments

Many people never manage OS themselves:

### AWS

```
EC2 GPU instance
Amazon Linux / Ubuntu
Docker
PyTorch
```

### Google Cloud

```
GKE
Vertex AI
Deep Learning VM
```

### Azure

```
Azure ML
GPU VM
```

---

## 7. For Apple Silicon Macs

People use:

```
macOS
 |
PyTorch MPS backend
 |
Metal GPU
```

Example:

```python
device = "mps"

model.to(device)
```

Good for:

* inference
* small models
* development

Not good for:

* large LLM training
* CUDA ecosystem

---

For your situation (RTX 4070 + LLM experiments), the typical stack would be:

```
Ubuntu 24.04
    |
NVIDIA Driver
    |
CUDA 12.x
    |
PyTorch
    |
Transformers / vLLM / SGLang / DeepSpeed
    |
LLM experiments
```

or:

```
Windows
 |
WSL2 Ubuntu
 |
same AI stack
```

Most LLM engineers today are effectively using **Ubuntu + Docker + CUDA**, regardless of the physical machine.
