---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla K80 与 llama.cpp 的限制
translated: true
type: note
---

问题：Tesla K80 24GB 能运行 llama.cpp 吗？

回答：

**技术上可以，但实际非常受限。** Tesla K80 可以运行一些老版本的 `llama.cpp` CUDA 构建，但对于现代 LLM 推理来说并不是一个好选择。

## 为什么可以运行

`llama.cpp` 主要需要：

1. CUDA 支持
2. GPU 计算内核
3. 足够的显存

K80 具备：

* CUDA 计算能力：**3.7**
* 总计 24GB 显存（2 × 12GB）
* FP16 支持（慢）

因此，一个启用了 CUDA 的老版本 `llama.cpp` 有可能为其编译。

示例：

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

make GGML_CUDA=1 \
     CUDA_DOCKER_ARCH=compute_37
```

关键部分是：

```bash
CUDA_DOCKER_ARCH=compute_37
```

因为 K80 是 `sm_37`。

## 大问题：现代 llama.cpp 已放弃老 GPU

现代 CUDA 工具链和内核越来越依赖更新的架构：

* CUDA 12 → 不再支持 Kepler
* CUDA 11.8 → 最后一个可行选项
* 更新的 PyTorch / CUDA 库 → 通常失败

你可能需要：

* 旧版 CUDA 工具包
* 旧版 NVIDIA 驱动
* 旧版 gcc

典型环境：

```
Ubuntu 20.04
CUDA 11.8
NVIDIA 驱动 470.xx
较旧的 llama.cpp 提交版本
```

## 显存现实

“24GB” 具有误导性：

```
K80
 ├── GPU0: 12GB
 └── GPU1: 12GB
```

`llama.cpp` 看到的是：

```
GPU0: 12GB
GPU1: 12GB
```

而不是：

```
GPU: 24GB
```

因此：

| 模型              | K80                         |
| ---------------- | --------------------------- |
| Llama 3.2 1B Q4  | ✅                           |
| Llama 3.2 3B Q4  | 可能                        |
| Llama 7B Q4      | 可能需 CPU 卸载              |
| Llama 8B Q4      | 困难                        |
| 13B+             | 主要靠 CPU                  |

一个 7B Q4 模型：

```
权重 ~4-5GB
KV 缓存 + 开销
```

可以放入一个 12GB GPU，但性能才是问题。

## 预期速度

粗略估计：

| GPU        | Llama 7B Q4 tok/s |
| ---------- | ----------------: |
| RTX 4090   |          100-200+ |
| RTX 3090   |            50-100 |
| RTX 4070   |             30-60 |
| Tesla P40  |             15-30 |
| Tesla K80  |              ~2-8 |

K80 有很多 CUDA 核心，但都是老旧的 Kepler 核心：

* 低频率
* 弱 FP16
* 无 Tensor Core
* 内存效率差

## 有趣的实验

对于你的 CUDA/内核学习，K80 实际上很有趣：

你可以尝试：

* CUDA 内核
* 内存带宽
* 多 GPU 分片
* llama.cpp 后端修改

架构很简单：

```
llama.cpp
    |
    +-- CUDA 内核
          |
          +-- sm_37
                |
                +-- GK210
```

但对于你的实际 LLM 实验室（nanochat、vLLM、SGLang、DeepSpeed），K80 基本上是一件博物馆藏品。

鉴于你目前拥有 RTX 4070 12GB，一块二手的 **RTX 3060 12GB** 作为第二块 GPU 可能比 K80 有用得多。它支持现代 CUDA，并且可以真正参与当前的 AI 工具链。
