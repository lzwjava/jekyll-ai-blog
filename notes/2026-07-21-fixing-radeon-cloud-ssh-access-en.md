---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Radeon Cloud SSH Access
translated: false
type: note
---

**Question: Why switching to Jupyter image and installing SSH server fixed access on Radeon Cloud?**

Answer:

Yes, your understanding is basically correct. On [Radeon Cloud](https://radeon-global.anruicloud.com/?tab=notebook&utm_source=chatgpt.com), different container images are not just different packages — they define the whole runtime environment.

The flow is roughly:

```
Radeon Cloud
      |
      v
GPU VM / container
      |
      +-- selected image
              |
              +-- JupyterLab?
              +-- SSH server?
              +-- vLLM?
              +-- model files?
              +-- tools?
```

The vLLM image is optimized for **serving models**, not necessarily interactive development. It may start:

```
vllm serve ...
```

but not include:

```
jupyter lab
sshd
terminal UI
```

The Jupyter image is more like a development workstation:

```
JupyterLab
 ├── Notebook
 ├── Terminal
 ├── Python environment
 ├── ROCm tools
 └── SSH (if installed)
```

The Radeon Cloud examples also use Jupyter as the entry point for vLLM experiments: for example, their Hermes + vLLM workshop instructs users to open a Jupyter terminal and start the vLLM server there. ([Radeon Cloud][1])

So your workaround:

```
switch image -> Jupyter notebook
        |
        v
apt install openssh-server
        |
        v
ssh into GPU machine
```

is a normal cloud workflow.

A typical setup:

```bash
sudo apt update
sudo apt install -y openssh-server

sudo mkdir -p /run/sshd

sudo service ssh start

ss -tlnp | grep :22
```

Then from your laptop:

```bash
ssh user@<gpu-instance-ip>
```

After SSH works, you can run:

```bash
tmux new -s vllm

vllm serve \
  Qwen/Qwen3-8B \
  --host 0.0.0.0 \
  --port 8000
```

The architecture becomes:

```
Laptop
  |
  | ssh
  v
Radeon Cloud GPU instance
  |
  +-- tmux
        |
        +-- vLLM server :8000
        |
        +-- ROCm
        |
        +-- AMD GPU
```

For hackathon work, I would usually choose:

* **Jupyter/Base image** → exploration, coding, debugging, SSH, agents
* **vLLM image** → final inference deployment/demo

because during development you need shell access much more often than a preconfigured inference server. Radeon Cloud provides both notebook-style environments and vLLM-focused templates. ([Radeon Cloud][2])

One thing to check: after installing SSH, make sure the container keeps the process alive. Some cloud containers restart when the main process exits. Running `sshd` under the platform's expected startup mechanism is safer than manually launching it.

[1]: https://radeon.anruicloud.com/templates/320/preview?utm_source=chatgpt.com "Notebook Preview - Radeon Cloud"
[2]: https://radeon.anruicloud.com/?utm_source=chatgpt.com "Radeon Cloud"
