---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building Preconfigured Ubuntu AI Agent Images
translated: false
type: note
---

Question: How to build a preconfigured Ubuntu image with Python, pip, and AI agent libraries already installed?

Answer:

For an AI agent server, the common pattern is **build a custom Ubuntu image → launch many identical machines**.

You have several options:

## Option 1: Packer (recommended for cloud images)

Use HashiCorp Packer to create a reusable Ubuntu image.

Architecture:

```
Ubuntu 24.04 base image
        |
        v
 Packer provisioning
        |
        +-- Python 3.12
        +-- uv/pip
        +-- PyTorch
        +-- agent libraries
        +-- system tools
        +-- configs
        |
        v
 ubuntu-ai-agent-v1 image
```

Example:

`ubuntu-agent.pkr.hcl`

```hcl
source "amazon-ebs" "ubuntu" {
  ami_name      = "ubuntu-ai-agent-v1"
  instance_type = "g6.xlarge"

  source_ami_filter {
    filters = {
      name = "ubuntu/images/*ubuntu-24.04-amd64-server-*"
    }
    owners = ["099720109477"]
  }

  ssh_username = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    script = "install.sh"
  }
}
```

`install.sh`

```bash
#!/bin/bash

set -eux

apt update

apt install -y \
    python3.12 \
    python3-pip \
    git \
    curl \
    build-essential

# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="/root/.local/bin:$PATH"

uv python install 3.12


# AI agent environment

uv venv /opt/agent-env

source /opt/agent-env/bin/activate


uv pip install \
    langchain \
    langgraph \
    openai \
    anthropic \
    pydantic \
    fastapi \
    uvicorn \
    transformers \
    torch


# your agent code

mkdir /opt/agent

git clone https://github.com/<YOUR_ORG>/<YOUR_AGENT>.git /opt/agent


chmod +x /opt/agent/start.sh
```

Build:

```bash
packer build ubuntu-agent.pkr.hcl
```

Now every new VM starts with:

```
Python ready
pip ready
AI libraries ready
agent code ready
```

---

## Option 2: Docker image (simplest)

For most agent workloads this is easier.

`Dockerfile`

```dockerfile
FROM ubuntu:24.04

RUN apt update && apt install -y \
    python3.12 \
    python3-pip \
    curl \
    git


RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"


WORKDIR /app

COPY requirements.txt .

RUN uv pip install \
    --system \
    -r requirements.txt


COPY agent ./agent


CMD ["python3", "agent/main.py"]
```

`requirements.txt`

```
langgraph
langchain
openai
anthropic
fastapi
uvicorn
transformers
torch
```

Build:

```bash
docker build -t my-ai-agent:v1 .
```

Run:

```bash
docker run \
 --gpus all \
 -p 8000:8000 \
 my-ai-agent:v1
```

---

## Option 3: Cloud-init image

For bare-metal / VPS:

Create:

```
ubuntu-agent.yaml
```

```yaml
#cloud-config

packages:
  - python3-pip
  - git
  - curl


runcmd:

  - curl -LsSf https://astral.sh/uv/install.sh | sh

  - pip install \
      langgraph \
      openai \
      anthropic

  - git clone https://github.com/<ORG>/<AGENT> /opt/agent
```

Then:

```bash
cloud-init init ubuntu-agent.yaml
```

---

## For your "AI employee / agent swarm" idea

I would build it like this:

```
                 Image Registry
                       |
        ubuntu-ai-agent:v1
                       |
       -------------------------------
       |              |              |
    Agent-1        Agent-2        Agent-3

       |
       +-- Python runtime
       +-- vLLM client
       +-- browser tools
       +-- MCP servers
       +-- vector DB client
       +-- your CLI agent
```

Version your images:

```
ubuntu-agent-v1
ubuntu-agent-v2
ubuntu-agent-v3
```

Never manually SSH and install packages.

---

For your use case (AI consulting + agent infrastructure), I would choose:

* **Docker** for development
* **Packer + Ubuntu image** for production GPU workers
* **Kubernetes** when you have many agents

The important idea: treat the whole AI agent environment as a **software artifact**, like a model checkpoint. Rebuild it deterministically.
