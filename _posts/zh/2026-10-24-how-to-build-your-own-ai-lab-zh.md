---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何搭建自己的AI实验室
translated: true
type: note
---

**问题：** 我是否有可能像 https://truth-lab.lzwjava.workers.dev 那样运行一个实验室？

**回答：**

是的——完全可行。这个网站是李智维的个人单人AI研究实验室，他使用的每个组件都是开源的或者可以二手买到。以下是现实可行的分解：

---

### 1. 网站本身（非常简单）
该网站托管在 Cloudflare Workers 上（`*.workers.dev`）——这意味着它是一个通过 Cloudflare 免费边缘网络提供的静态页面。你可以克隆他的做法：
- 一个免费的 Cloudflare Workers 账户
- 一个 HTML/CSS 文件（无需后端）
- 零托管成本

---

### 2. GPU 硬件（中等成本，中等难度）
他用三台二手数据中心工作站构建了一个 52 GB CUDA VRAM 集群——Tesla M40 12 GB、M40 24 GB 和 P100 16 GB——大约 100 人民币/GB VRAM。12 GB 大约 140 美元。难点在于：让它工作需要进行 BIOS 考古——具体来说是在 MSI Z170A Gaming M5 主板上启用 Above 4G Decoding、禁用 CSM，并将 M40 放在 CPU 直连的 x16 PCIe 插槽中。

对于更简单的起步，**一张 RTX 4070（12 GB，全新约 400–600 美元）** 就能走得很远。他大部分训练运行就用了这张卡。

---

### 3. 训练小型 LLM（可学习，耗时数周到数月）
他从零开始在 FineWeb、OpenWebText 和 SEC 文件上预训练了 124M 和 760M 参数的 GPT-2——不是从检查点开始。所有工具都是开源的：
- **nanoGPT**（Karpathy 的仓库，他的 45 次提交 fork 是公开的）
- **PyTorch** + 标准 Python 栈
- 公开数据集（FineWeb、OpenWebText、Wikipedia 转储）

SEC-EDGAR-GPT 模型在单张 RTX 4070 上大约花了 8 小时，整个流程——训练、论文、聊天机器人、网站——借助 AI 编码助手在三天内完成。

---

### 4. 推理服务（中等难度）
他运行 vLLM、SGLang（从源码编译）和 llama.cpp，在本地提供 Qwen3-0.6B 和 DeepSeek-R1-14B GGUF 等开放模型的服务。全部免费且文档齐全。主要障碍是 CUDA 环境设置，特别是对于较旧的 GPU 架构如 M40（Maxwell，CC 5.2）。

---

### 5. 你实际需要什么

| 组件 | 最低起步配置 | 成本 |
|---|---|---|
| 网站 | Cloudflare Workers（免费） | $0 |
| GPU | RTX 4070 12 GB（或租用 RunPod/Lambda） | $400–600 或约 $1–3/小时 |
| 训练 | nanoGPT + PyTorch + 公开数据集 | 软件 $0 |
| 服务 | llama.cpp 或 vLLM | 软件 $0 |
| 技能 | Python、Linux、基本 ML 概念 | 时间 |

---

### 结论

**网站**只需一个下午。**实验室**（实际的 GPU 工作）如果你有一些工程背景，几个月内确实可行——他是在白天工作之余完成的。他的真实教训：在投入 GPU 时间之前先验证代码、环境和数据——一个破损的流水线总是在训练时失败。云 GPU（RunPod、Lambda）让你完全可以跳过硬件直接开始。

**参考资料：**
- [真理实验室 — 李智维](https://truth-lab.lzwjava.workers.dev)
- [lzwjava/nanoGPT (GitHub)](https://github.com/lzwjava/nanoGPT)
- [lzwjava/sec-edgar-gpt (GitHub)](https://github.com/lzwjava/sec-edgar-gpt)