---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'FreeToken: MoE推理引擎'
translated: true
type: note
---

问题：**`FlashML-org/FreeToken` 是什么？**

答案：**FreeToken 本质上是一个推理引擎，用于在显存不足的硬件上运行超大型 MoE 大语言模型。**

其核心思想是：

> **将模型频繁使用的部分放在 GPU 上，将庞大的 MoE 专家权重保留在 CPU 内存中，仅在需要时通过 PCIe 进行流式传输和缓存专家。**

因此，它有点类似于 **vLLM/SGLang + 智能 CPU/PCIe 卸载**，但专门针对 **消费级/工作站 GPU 上的大型 MoE 模型** 而设计。（[GitHub][1]）

### 它解决的问题

假设你有：

```text
290B 参数 MoE 模型

GPU 显存：      24 / 48 / 96 GB
CPU 内存：      128 / 256 GB
```

你显然无法将所有 290B 的权重放入显存。

但在 MoE 模型中，每个 token 只激活少量专家：

```text
                 290B 总参数
                         │
             ┌───────────┴───────────┐
             │                       │
       共享/密集部分              数千个专家
             │                       │
             ▼                       ▼
          GPU 显存               CPU 内存
                                  │
                                  │ PCIe
                                  ▼
                                GPU
                        仅选中的专家
```

FreeToken 围绕这种架构构建了运行时。

其 README 明确将其描述为一种 **"边缘原生的混合专家服务引擎"**，将 GPU、CPU、主机内存和互连视为一个推理平台。（[GitHub][1]）

---

## 有趣的部分：专家卸载

想象一个 MoE 层：

```python
router(x)
    ↓
专家 17
专家 83
专家 421
专家 912
    ↓
加权求和
```

FreeToken 可以将这些专家保留在主机内存中：

```text
内存
┌──────────────────────────────────────────┐
│ 专家 0                                   │
│ 专家 1                                   │
│ 专家 2                                   │
│ ...                                      │
│ 专家 421  ← 需要                         │
│ ...                                      │
└──────────────────────────────────────────┘
                  │
               PCIe Gen5
                  │
                  ▼
GPU
┌──────────────────────────────────────────┐
│ 当前需要的专家缓存                      │
│ 专家 421                                │
│ 专家 83                                 │
│ ...                                      │
└──────────────────────────────────────────┘
```

然后它使用 **LRU 专家缓存**、CPU/GPU 协同执行和带宽感知调度来减少移动权重的成本。（[GitHub][1]）

这与你一直在实验的内容高度相关：**GPU 显存 + 主机内存 + PCIe 作为一个有效的内存层次结构。**

---

## 为什么这与普通的 vLLM 不同

可以将设计空间想象成这样：

```text
llama.cpp
    │
    ├── CPU/GPU 混合
    │
    ▼
vLLM / SGLang
    │
    ├── 以 GPU 为中心的服务
    │
    ▼
FreeToken
    │
    └── 以 MoE 为中心的异构服务
          GPU + CPU + 内存 + PCIe
```

FreeToken 特别关注以下情况：

```text
RTX 4090 / 5090 / RTX 6000 Pro
              +
128–512 GB 系统内存
              +
PCIe Gen4/Gen5
              ↓
       巨大的 MoE 模型
```

而不是要求：

```text
8 × H100/H200
```

该项目目前目标是 NVIDIA Ampere 及更新的 GPU，需要驱动 580+ / CUDA 13。（[GitHub][2]）

---

## 它不仅仅是一个卸载器

其中包含几个有趣的系统设计思路。

### 1. 带宽自适应执行

FreeToken 有一个 `q*` 策略，根据可用带宽决定在 CPU 上执行多少工作，在 GPU 上执行多少工作。

概念上：

```text
                ┌── GPU 计算
MoE 专家 ─────┤
                └── CPU 计算

        根据以下选择

GPU FLOPS
PCIe 带宽
CPU 内存带宽
专家大小
批处理大小
```

这一点很重要，因为 **PCIe 很容易成为瓶颈**。

例如：

```text
GPU 计算：         巨大
PCIe Gen5 x16：     理论 ~64 GB/s
CPU 内存：         数百 GB/s
```

有时：

```text
加载专家 → GPU → 计算
```

比简单地：

```text
在 CPU 上计算专家
```

还要慢。

因此 FreeToken 具有：

```bash
ft bench bw
```

用于测量 CPU/PCIe 带宽并生成运行时使用的硬件特定配置文件。（[GitHub][3]）

---

### 2. 双缓冲预填充

在预填充期间，它可以重叠：

```text
GPU 计算专家 N
        │
        ├───────────────┐
        │               │
        ▼               ▼
     计算          PCIe 传输
                    专家 N+1
```

因此 PCIe 传输不一定完全与 GPU 计算串行化。

这是一个经典的系统优化：

```text
while GPU 计算:
    DMA 下一个专家
```

---

### 3. 动态显存分配

这是另一个有趣的功能。

FreeToken 可以在不重启引擎的情况下，动态重新平衡以下两者之间的显存分配：

```text
MoE 专家缓存
        ↕
KV 缓存
```

（[GitHub][1]）

所以概念上：

```text
显存 = 96 GB

┌──────────────────────┐
│ 专家缓存    70 GB    │
│ KV 缓存     26 GB    │
└──────────────────────┘

              ↓ 长上下文

┌──────────────────────┐
│ 专家缓存    45 GB    │
│ KV 缓存     51 GB    │
└──────────────────────┘
```

---

## 它也有自己的权重格式

FreeToken 引入了 **FTW**，其快速权重格式。

你可以转换 Hugging Face 检查点：

```bash
ft checkpoint \
    --model <hf_model> \
    --out <ftw_dir>
```

然后：

```bash
ft serve --model <ftw_dir>
```

FTW 格式专门为 MoE 专家的快速加载/卸载而设计。（[GitHub][3]）

---

## API 兼容性很不错

它暴露了以下接口：

```text
OpenAI API
/v1/chat/completions
/v1/responses

Anthropic API
/v1/messages
```

因此现有客户端基本上可以指向：

```text
http://localhost:1919
```

而不是 OpenAI/Anthropic 端点。（[GitHub][4]）

它甚至有：

```bash
ft launch claude
ft launch codex
ft launch opencode
ft launch openclaw
```

用于将编码代理直接连接到本地模型服务器。（[GitHub][4]）

---

# 硬件角度对你来说可能最有趣

你之前关于：

```text
GPU 显存
   +
系统内存
   +
PCIe
   +
大型 MoE
```

的想法基本上正是 FreeToken 要解决的问题。

例如：

```text
RTX PRO 6000
96 GB 显存
        +
256 GB DDR5 内存
        +
PCIe Gen5 x16
        ↓
大型 NVFP4 MoE
```

与其想：

> "我的 GPU 只有 96 GB，因此我无法运行 200-300B 的模型。"

FreeToken 的理念是：

> **显存是一个缓存，而不是整个模型的内存。**

这是一个非常重要的概念转变。

README 说它的目标是 **在消费级硬件上运行 290B+ 前沿 MoE 模型**，并支持 **MXFP4、NVFP4、FP8 和 BF16** 等格式。（[GitHub][1]）

---

## 当前软件栈

实现相当底层：

```text
Python
  │
  ├── PyTorch 2.11
  ├── Triton 3.6
  ├── FlashInfer
  ├── SGLang 内核
  │
  └── 自定义 C++/CUDA 扩展
             │
             ▼
          NVIDIA GPU
```

仓库的构建配置明确要求 Torch 2.11.x 和 CUDA 13 工具链，并带有用于锁页内存和 CPU MoE 执行的原生 C++ 扩展。（[GitHub][5]）

---

## 支持的模型

该项目列出的模型包括：

```text
DeepSeek-V4
GLM-5.2
GLM-4.7
Qwen3.8-Flash-Next
Qwen3.6 / Qwen3.5 MoE
Qwen3.8 / Qwen3.6 密集模型
```

使用各种 FP8/NVFP4/BF16 检查点。（[GitHub][6]）

---

# 一张图总结

我会将 FreeToken 概括为：

```text
                    FreeToken
                       │
       ┌───────────────┼────────────────┐
       │               │                │
     模型            调度器            内存
       │               │                │
       ▼               ▼                ▼
   巨大的 MoE      带宽感知执行      显存缓存
       │                                │
       │                                │
       └──────────────┬─────────────────┘
                      │
              PCIe / CPU 内存
                      │
                      ▼
              消费级 GPU
```

**它不是一个新的 LLM。它是一个 LLM 推理运行时。**

从技术上讲，我认为这个仓库中最值得研究的东西不是 CLI 或 API——而是 **MoE 专家缓存 + CPU/GPU 执行 + PCIe 调度路径**。那里才是有趣的系统工作所在。

[FreeToken GitHub 仓库](https://github.com/FlashML-org/FreeToken?utm_source=chatgpt.com) [FreeToken 论文 (arXiv)](https://arxiv.org/abs/2608.16157?utm_source=chatgpt.com)

[1]: https://github.com/FlashML-org/FreeToken/blob/main/README.md?utm_source=chatgpt.com "FreeToken/README.md at main · FlashML-org/FreeToken · GitHub"
[2]: https://github.com/FlashML-org/FreeToken/issues/84?utm_source=chatgpt.com "FAQ · Issue #84 · FlashML-org/FreeToken · GitHub"
[3]: https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md?utm_source=chatgpt.com "FreeToken/docs/cli.md at main · FlashML-org/FreeToken · GitHub"
[4]: https://github.com/FlashML-org/FreeToken/blob/main/docs/quickstart.md?ref=explainx&utm_source=chatgpt.com "FreeToken/docs/quickstart.md at main · FlashML-org/FreeToken · GitHub"
[5]: https://github.com/FlashML-org/FreeToken/blob/main/pyproject.toml?utm_source=chatgpt.com "FreeToken/pyproject.toml at main · FlashML-org/FreeToken · GitHub"
[6]: https://github.com/FlashML-org/FreeToken/blob/main/docs/models.md?utm_source=chatgpt.com "FreeToken/docs/models.md at main · FlashML-org/FreeToken · GitHub"