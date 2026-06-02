---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD开发者云GPU Droplet指南
translated: true
type: note
---

问题：什么是基于Ubuntu 24.04和ROCm 7.2的AMD开发者云GPU Droplet？使用它需要了解什么？

答案：

## AMD开发者云 — GPU Droplet概述

您的Droplet（`7.2-gpu-mi300x1-192gb-devcloud-atl1`）是一个**单块AMD Instinct MI300X GPU实例**，托管在**ATL1（亚特兰大）**区域，由AMD开发者云提供支持。以下是您需要了解的所有信息：

---

### 这是什么

AMD开发者云可通过 `devcloud.amd.com` 访问，并依赖DigitalOcean提供云环境，最终部署GPU Droplet。您可以创建单块GPU AMD Instinct MI300X或8×GPU Instinct MI300X实例。

您的具体Droplet规格：

- **GPU：** 1× AMD Instinct MI300X
- **显存：** 192 GB
- **操作系统：** Ubuntu 24.04 LTS
- **软件栈：** ROCm 7.2
- **区域：** ATL1（亚特兰大）

---

### ROCm 7.2 — 它的能力

ROCm 7相较于前代带来了突破性的性能提升——训练工作负载相比ROCm 6基准测试平均提升高达3倍，推理性能平均提升4.6倍。这些提升得益于GPU利用率优化、对低精度数据类型的支持以及优化的数据传输。

AMD ROCm是一个开放的软件栈，包括驱动程序、开发工具和API，支持从底层内核到最终用户应用的GPU编程。ROCm针对生成式AI和HPC应用进行了优化，并且可以轻松将现有代码迁移到ROCm软件中。

---

### Droplet就绪后的第一步

#### 1. 应用安全更新（按仪表板提示操作）

通过SSH登录您的Droplet并运行：

```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

#### 2. 通过SSH连接

```bash
ssh root@<your-droplet-ip>
```

#### 3. 验证GPU是否被检测到

```bash
rocm-smi
```

这是AMD版本的 `nvidia-smi`。您将看到GPU利用率、显存使用情况和温度。

#### 4. 进入预构建的Docker容器（如果使用快速启动镜像）

```bash
docker exec -it rocm /bin/bash
```

---

### 运行模型（例如，使用vLLM）

您可以在容器内启动vLLM API服务器，如下所示：

```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-1.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype float16 \
  > /tmp/vllm.log 2>&1 &
```

该模型从HuggingFace免费下载，无需认证，在MI300X的192 GB显存中几秒内加载完成，并原生支持OpenAI聊天格式。

---

### 重要：计费提醒

即使Droplet已关机，您仍会被计费。要完全停止计费，您必须从仪表板**销毁**Droplet，而不仅仅是关机。

您当前状态显示 **“正在关机 / 活动”** —— 这意味着在完全销毁或您有意停止使用之前，它仍在产生费用。

---

### 定价参考

单块MI300X实例的标准定价为**每小时1.99美元**，8×MI300X实例为**每小时15.92美元**。

---

### 开箱即用的可用框架

除了开箱即用地支持ROCm部署外，还提供了针对JAX、Megatron、PyTorch、SGLang和vLLM的快速启动包。

---

### 免费额度

AMD AI开发者计划为成员提供100美元的免费AMD开发者云额度，足以支持约50小时的初始使用。展示有用应用并公开分享项目的成员还可以申请额外额度。

参考资料：

- [如何在AMD开发者云上开始使用](https://www.amd.com/en/developer/resources/technical-articles/2025/how-to-get-started-on-the-amd-developer-cloud-.html)
- [AMD开发者云教程：在AMD GPU上托管您的第一个LLM](https://lablab.ai/ai-tutorials/amd-developer-cloud-host-llm-vllm)
- [试用AMD开发者云 — Phoronix评测](https://www.phoronix.com/review/amd-developer-cloud)
- [用开放软件加速AI：AMD ROCm 7来了](https://www.amd.com/en/solutions/data-center/insights/accelerating-ai-with-open-software-amd-rocm-7-is-here.html)
- [OpenClaw在AMD开发者云上：使用Qwen 3.5和SGLang免费部署](https://www.amd.com/en/developer/resources/technical-articles/2026/openclaw-on-amd-developer-cloud-qwen-3-5-and-sglang.html)
