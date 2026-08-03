---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建预配置的Ubuntu AI代理镜像
translated: true
type: note
---

问题：如何构建一个预配置的Ubuntu镜像，其中已安装Python、pip和AI代理库？

答案：

对于AI代理服务器，常见的模式是**构建自定义Ubuntu镜像 → 启动许多相同配置的机器**。

你有以下几种选择：

## 选项1：Packer（推荐用于云镜像）

使用HashiCorp Packer创建可复用的Ubuntu镜像。

架构：

```
Ubuntu 24.04 基础镜像
        |
        v
 Packer 配置
        |
        +-- Python 3.12
        +-- uv/pip
        +-- PyTorch
        +-- 代理库
        +-- 系统工具
        +-- 配置文件
        |
        v
 ubuntu-ai-agent-v1 镜像
```

示例：

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

# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="/root/.local/bin:$PATH"

uv python install 3.12


# AI代理环境

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


# 你的代理代码

mkdir /opt/agent

git clone https://github.com/<YOUR_ORG>/<YOUR_AGENT>.git /opt/agent


chmod +x /opt/agent/start.sh
```

构建：

```bash
packer build ubuntu-agent.pkr.hcl
```

现在每个新虚拟机启动时都包含：

```
Python 就绪
pip 就绪
AI 库就绪
代理代码就绪
```

---

## 选项2：Docker镜像（最简单）

对于大多数代理工作负载，这种方式更简单。

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

构建：

```bash
docker build -t my-ai-agent:v1 .
```

运行：

```bash
docker run \
 --gpus all \
 -p 8000:8000 \
 my-ai-agent:v1
```

---

## 选项3：Cloud-init镜像

适用于裸金属 / VPS：

创建：

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

然后：

```bash
cloud-init init ubuntu-agent.yaml
```

---

## 针对你的"AI员工/代理集群"构想

我会这样构建：

```
                 镜像仓库
                     |
      ubuntu-ai-agent:v1
                     |
     -------------------------------
     |              |              |
  Agent-1        Agent-2        Agent-3

     |
     +-- Python 运行时
     +-- vLLM 客户端
     +-- 浏览器工具
     +-- MCP 服务器
     +-- 向量数据库客户端
     +-- 你的 CLI 代理
```

对镜像进行版本管理：

```
ubuntu-agent-v1
ubuntu-agent-v2
ubuntu-agent-v3
```

永远不要手动通过SSH安装包。

---

针对你的使用场景（AI咨询 + 代理基础设施），我会选择：

* **Docker** 用于开发
* **Packer + Ubuntu镜像** 用于生产环境GPU工作节点
* **Kubernetes** 当你有大量代理时

重要的理念：将整个AI代理环境视为一个**软件制品**，就像模型检查点一样。以可重复的方式构建它。
