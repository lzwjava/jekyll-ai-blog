---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'CMP 170HX: 穷人的A100'
translated: true
type: note
---

## 问题：NVIDIA CMP 170HX 介绍——"近乎 A100"的AI加速器

![Image](https://images.openai.com/static-rsc-4/FHSdxFOE8fxE-hoZI4SdzM9KJtemCgANadIzjqS2C8S0AgUu_-A-1suKUgg0RhCt4ADsdheg6gmNwUSzt7rq8SF5dctPYcyq5lXRBssuhAEqXksNta-cyUvXbCp_5a2QeR1CijhB0c5cUBbsKPp1eEPh3ZRz_jEjoJx_DIXL6cC41RxLV_i4IG6N3D1OTBy-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Hoz66izlEFDWn_7iO41vBUEBTtVFWVwcMUKqRlnPdCuXsIpGoXuKqUGu9COpsslIfvkdVo0vn0fT69LzuIvOAqWwAXbI1z8qJmoaTtG9KoEGxrhiZFrJtwAvrbylvPmKGedZ6Nx9IP4uXUwFIhTvKeb1p3FEwWaW-3VrNiTT4ffldLTWX2TqfKeMUyiWMmwq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dFl_Br3HhcE1_7mV8dWBf3e_KTyUardboGd8cSE0J7sOMXV5_rxFJVe0dB3TD0K5t6CaZm9HN3K4pZ5CzwD7ViEEf29DmG3RQ1hrL75j-e6R-XUqBtxbClj5h5NJfZzXMI1eXGaSig33gxfCGW_n2XzWSenjDlNcri4WnZ81MvItEif_9T4GJOc5V99VNDrC?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5edu3VZlo_pcU8aeIJlabW4Lx0UHAfvsBc7IWcjLX3l2bD5MZylbR2Ct_hlPYJaAKdtOpvotVh5G2Kd6rg7rTkAYlWzcxmh8Cxx6ooMVNnKZPR0jG7YmNj6_BT7t0h7q2jT1SDlTV1pjTao2nQXOvjZiiWhC3ixQPiW8ULL5quAMVf8HtLrhd3d3WRAX0iR3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NMjq2gCfMiaNKijfXyoIAmNqwKWJGOIhp4vsLaUlLUdaWdKVddLFvZuft-mQI3u_hX9yHjQ1AtDeDZErNthSfQy9MAmi4xUdVmw6T-QtJGbuCr-hYzNbdQOk75Vk9IHx4xou0ipzujffnbsEN-X-Du5NyzZLqYrmqxFPA1OZA3_RBvLwPEz_1I2YZUVBDEGB?purpose=fullsize)

## 答案

**NVIDIA CMP 170HX** 是二手市场上最有趣的“意外AI GPU”之一。

简短来说：

> CMP 170HX = 一块精简版的 NVIDIA A100 (GA100) 芯片，最初用于加密货币挖矿，但最近通过软件解锁，变成了一个约 64GB HBM2e 的 AI 加速器。([DevQuasar][1])

它基本上就是一块 **“穷人的 A100”**。

---

## 1. 起源：NVIDIA 为什么制造它

大约在 2021 年，加密货币挖矿热潮期间，NVIDIA 推出了 **CMP (Cryptocurrency Mining Processor)** 产品线。

CMP 170HX 使用了相同的：

* GPU 架构：**Ampere**
* 芯片：**GA100**
* 工艺：TSMC 7nm
* 内存类型：**HBM2e**

同系列还驱动着著名的：

* NVIDIA A100 40GB
* NVIDIA A100 80GB

([DevQuasar][1])

但 NVIDIA 故意对其进行了限制：

| 特性                | A100 PCIe | CMP 170HX       |
| ------------------- | --------- | --------------- |
| GPU 芯片            | GA100     | GA100           |
| CUDA 架构           | SM80      | SM80            |
| HBM2e               | 40/80GB   | 8/10GB 暴露     |
| 内存总线            | 5120-bit  | 4096-bit        |
| PCIe                | Gen4 x16  | Gen1 x4         |
| Tensor 性能         | 完整      | 严重受限        |
| 显示输出            | 无        | 无              |

([DevQuasar][1])

---

## 2. 为什么它在 2026 年出名了

有趣的发现：

硬件并没有完全被阉割。

NVIDIA 主要使用了：

* 固件限制
* 熔丝配置
* 保护寄存器

来禁用：

* 内存容量
* 计算单元
* PCIe 速度

GPU 物理上仍然拥有更多能力。

([DevQuasar][1])

社区发现，使用以下工具可以绕过限制：

* NVIDIA 开源内核驱动
* 固件漏洞利用技术
* 像 `cmpunlocker` 这样的工具

解锁后：

例如 8GB CMP 170HX：

```
解锁前：

VRAM: 8GB
计算: 受限
PCIe: Gen1 x4


解锁后：

VRAM: 约 64GB HBM2e
计算: 接近 A100
PCIe: Gen2 x4
```

([GitHub][2])

---

## 3. 为什么 64GB HBM2e 对 AI 来说很重要

对于 LLM 推理，VRAM 往往是瓶颈。

例如：

### Qwen / Llama 风格模型

大致内存需求：

```
7B 模型 FP16：
约 14GB

14B FP16：
约 28GB

32B FP16：
约 64GB
```

因此，一块解锁后的 CMP 170HX 有可能运行：

* 30B 级别 FP16 模型
* 70B 级别量化模型
* 大型嵌入模型
* 推理服务器

重要的不是原始 TFLOPS。

而是：

> “我能不能把模型塞进一张 GPU 里？”

一张 24GB 的 RTX 4090 更快，但一张 64GB 的 CMP 170HX 能容纳更大的模型。

---

## 4. 性能对比

大致概念：

| GPU                | VRAM        | AI 实用性                    |
| ------------------ | ----------- | ---------------------------- |
| RTX 4090           | 24GB GDDR6X | 非常快，容量有限             |
| RTX 3090           | 24GB        | 很好的业余 AI GPU            |
| RTX 6000 Ada       | 48GB        | 专业级                       |
| CMP 170HX 解锁后   | 64GB HBM2e  | 廉价大内存 AI                |
| A100 40GB          | 40GB HBM2   | 数据中心                     |
| A100 80GB          | 80GB HBM2e  | 数据中心                     |

CMP 170HX 优势：

* 巨大内存带宽
* HBM
* 类似 ECC 的数据中心设计
* 64GB 容量

缺点：

* 较老的 Ampere 架构
* 无 NVLink
* PCIe 带宽差
* 被动散热
* 奇怪的电源接口

([GitHub][2])

---

## 5. 硬件细节

这张卡很特别：

```
GA100 GPU
 |
 +-- HBM2e 堆栈
 |
 +-- 被动散热片
 |
 +-- EPS 8-pin 电源
 |
 +-- 无显示输出
```

它是为矿场设计的。

8GB 版本：

```
PCI ID: 10de:20c2
解锁：
8GB -> 64GB
```

10GB 版本：

```
PCI ID: 10de:2082
解锁：
10GB -> 40GB
```

重要：它们不同。不要以为所有 CMP 170HX 都能变成 64GB。([GitHub][2])

---

## 6. 针对你的 AI 工作站使用场景

鉴于你的实验：

* GPT-2 训练
* Qwen 模型
* vLLM
* llama.cpp
* 本地推理

CMP 170HX 实际上非常有趣。

例如：

你的 RTX 4070 Ti：

```
12GB VRAM
CUDA 8.9
速度快
```

CMP 170HX：

```
64GB VRAM
CUDA 8.0
计算较慢
内存巨大
```

对于：

✅ QLoRA
✅ 推理
✅ 运行更大的模型
✅ 实验 30B/70B 量化模型

CMP 170HX 可能更有用。

对于：

❌ 图像生成速度
❌ CUDA 内核优化
❌ 快速训练小模型

RTX 4070/4090 更好。

---

## 7. 目前市场情况

解锁前：

```
$250 - $500
```

发现后：

```
$1000 - $2000+
```

因为人们意识到：

```
廉价矿卡
        ↓
A100 芯片
        ↓
64GB HBM AI 加速器
```

([Niconiconi][3])

---

## 我的看法

CMP 170HX 很可能是近年来最大的“隐藏AI硬件套利”发现之一。

它并非 H100/B200 的替代品。

但对于本地 AI 工程师来说：

```
$1000 解锁后的 CMP 170HX
vs
$5000+ 二手 A100
```

性价比极具吸引力。

主要风险：

1. 散热（被动散热矿卡）
2. 驱动兼容性
3. 二手矿卡损耗
4. 解锁软件成熟度

对于像你这样构建本地 LLM 系统的人来说，这张卡比普通游戏 GPU 有趣得多，因为 **VRAM 容量决定了你能运行哪些模型**。

[1]: https://devquasar.com/hardware/the-almost-a100-nvidia-cmp-170hx/?utm_source=chatgpt.com "The almost A100 – NVIDIA CMP 170HX – DevQuasar"
[2]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/hardware/board-and-variants.md?utm_source=chatgpt.com "cmp170hx/docs/hardware/board-and-variants.md at main · Consensus-Protocol/cmp170hx · GitHub"
[3]: https://niconiconi.neocities.org/tech-notes/nvidia-cmp-170hx-review/?utm_source=chatgpt.com "All GB/s without FLOPS - Nvidia CMP 170HX Review, Performance Lockdown Workaround, Teardown, Watercooling, and Repair"
