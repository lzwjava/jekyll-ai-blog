---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nvidia Tesla M40与M60对比
translated: true
type: note
---

问题：对比 NVIDIA Tesla M60 和 M40 显卡芯片。

答案：

Tesla **M40** 和 **M60** 都是 2015 年前后的 **Maxwell 架构（计算能力 5.2）** Tesla 显卡，但它们的用途不同。M40 是 **面向计算/AI 的单一大 GPU**，而 M60 基本上是 **面向虚拟化/图形的双小 GPU**。（[NVIDIA Docs][1]）

|                  | Tesla M40                      | Tesla M60                 |                 |
| ---------------- | ------------------------------ | ------------------------- | --------------- |
| 架构             | Maxwell GM200                  | 2 × Maxwell GM204         |                 |
| 用途             | HPC / 机器学习计算             | VDI / 虚拟工作站           |                 |
| CUDA 核心数      | 3072                           | 4096 总计（2048 × 2）      |                 |
| 显存             | 12GB 或 24GB GDDR5             | 16GB GDDR5（每 GPU 8GB）   |                 |
| 显存位宽         | 384-bit                        | 2 × 256-bit               |                 |
| 显存带宽         | ~288 GB/s                      | ~320 GB/s 总计             |                 |
| FP32             | ~6.8 TFLOPS                    | ~9.6 TFLOPS 总计           |                 |
| TDP              | 250W                           | 300W                      |                 |
| PCIe             | PCIe 3.0 x16                   | PCIe 3.0 x16              |                 |
| GPU 数量         | 1 颗芯片                       | 2 颗芯片                   | ([Microway][2]) |

## 芯片差异

### Tesla M40

```
GM200
 |
 +-- 24 SM
 |
 +-- 3072 CUDA 核心
 |
 +-- 12/24GB GDDR5
```

它与 Titan X Maxwell 属于同一 GPU 家族。

优点：

* 单一大 GPU 显存空间
* 存在 24GB 版本
* 更适合 CUDA 计算
* 更适合 LLM 推理实验（在 Maxwell 架构的限制范围内）

缺点：

* 架构老旧
* 不支持 FP16 加速（对现代 LLM 很重要）
* 无 Tensor Core
* 仅支持计算能力 5.2

### Tesla M60

```
GPU0: GM204 8GB
GPU1: GM204 8GB

总计：
16GB 显存
4096 CUDA 核心
```

操作系统将其识别为 **两个独立的 GPU**，而非一个 16GB 的 GPU。

示例：

```bash
nvidia-smi

GPU 0: Tesla M60 8192 MiB
GPU 1: Tesla M60 8192 MiB
```

你无法在“M60 16GB”上运行需要 12GB 显存的模型，因为每个 GPU 只有 8GB 显存。

适合：

* 多用户场景
* VDI
* 渲染
* 并行的小型工作负载

不适合：

* LLM 推理
* 需要统一显存的大型 CUDA 工作负载

（[NVIDIA][3]）

## 用于 llama.cpp / LLM 使用

两者对比：

### M40 24GB 胜出

示例：

```
M40 24GB
        |
        | llama.cpp
        |
        +-- 13B Q4 模型（约 8GB）
        +-- 30B Q4 模型（约 18GB）
```

M60：

```
M60

GPU0 8GB
GPU1 8GB

无法轻松合并

```

13B 模型可能可以放入单个 M60 GPU，但如果软件不支持多 GPU 拆分，第二个 GPU 就会被浪费。

## AI 性能对比

近似值：

```
现代 RTX 4090

FP16 Tensor：
330+ TFLOPS

Tesla M40：

FP32：
6.8 TFLOPS

Tesla M60：

FP32：
9.6 TFLOPS
```

差距巨大，因为 Maxwell 没有 Tensor Core。

对于 LLM：

```
RTX 3090 24GB
    >>> M40 24GB
    >>> M60
```

但若用于低成本实验：

```
M40 24GB：
显存/价格比高

M60：
主要用于 GPU 维修/测试
```

## 电源 / 硬件

M40：

* 需要强劲的电源
* 通常为被动散热
* 需要服务器风道

M60：

* 也是服务器显卡
* 300W
* 双 GPU 意味着更高的热量密度

两者共同点：

* 无显示输出
* PCIe x16
* 需要旧版 NVIDIA 驱动

（[NVIDIA][3]）

## 我对你的 GPU 实验室 / LLM 实验的排名

鉴于你对 llama.cpp、nano-vLLM、旧款 Tesla 显卡的兴趣：

```
Tesla P40 24GB  >>>  Tesla M40 24GB  >>>  Tesla M60  >>> Tesla K80
```

原因：

* P40：Pascal 架构，24GB，CUDA 支持更好
* M40：Maxwell 架构，但单 GPU 24GB
* M60：两个 8GB GPU
* K80：2×12GB，但 Kepler 架构非常慢

对于本地 LLM 实验，M40 24GB 实际上比 M60 更值得被称为“廉价显存怪兽”。

[1]: https://docs.nvidia.com/datacenter/tesla/pdf/NVIDIA_Data_Center_GPU_Driver_Release_Notes_450_v6.0.pdf?utm_source=chatgpt.com "NVIDIA Data Center GPU Driver version 450.156.00 (Linux) / 453.23 (Windows)"
[2]: https://www.microway.com/knowledge-center-articles/in-depth-comparison-of-nvidia-tesla-maxwell-gpu-accelerators/?utm_source=chatgpt.com "In-Depth Comparison of NVIDIA Tesla \"Maxwell\" GPU Accelerators - Microway"
[3]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/nvidia-m60-datasheet.pdf?ncid=no-ncid&utm_source=chatgpt.com "Data Sheet: Tesla M60"
