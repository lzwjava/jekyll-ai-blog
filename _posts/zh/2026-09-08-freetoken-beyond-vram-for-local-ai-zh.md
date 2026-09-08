---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'FreeToken: 超越VRAM的本地AI'
translated: true
type: note
---

问题：**FreeToken 将如何影响本地模型服务的趋势以及更广泛的 AI 生态系统？**

答案：

我认为 **FreeToken 作为一种方向比它作为一个服务引擎本身更重要**。

核心思想是：

> **未来“GPU 内存”的定义将变得不如“总本地内存带宽 + 互连 + 计算”重要。**

FreeToken 明确将 **GPU 显存 + 系统内存 + CPU + PCIe** 视为一台推理机器，而不是假设整个模型必须放入显存内。其论文报告称，可在游戏台式机上运行 **284B** 的模型，在单工作站 GPU 上运行 **753B GLM-5.2**。([arXiv][1])

---

## 1. 旧的本地 LLM 模式

从历史上看，本地服务的模式大致如下：

```text
                GPU 显存
       ┌──────────────────────┐
       │ 整个模型             │
       │ KV 缓存              │
       │ 激活值               │
       └──────────────────────┘
                 │
              计算
                 │
              tokens
```

因此人们自然会问：

```text
"我的 RTX 4090 24GB 能跑这个模型吗？"
```

如果：

```text
模型大小 > 显存
```

你基本上就没办法了，或者只能接受巨大的 CPU 卸载惩罚。

这就造成了我们熟悉的执念：

```text
12 GB → 16 GB → 24 GB → 48 GB → 80 GB → 96 GB → 192 GB
```

---

# 2. FreeToken 改变了思维模型

对于 MoE：

```text
                系统内存
        ┌─────────────────────────┐
        │ Expert 0               │
        │ Expert 1               │
        │ Expert 2               │
        │ ...                    │
        │ Expert N               │
        └────────────┬────────────┘
                     │ PCIe
                     ▼
              ┌──────────────┐
              │ GPU 显存      │
              │              │
              │ 热门 experts │
              │ KV 缓存      │
              │ 共享组件     │
              └──────┬───────┘
                     │
                     ▼
                  Tensor Cores
```

MoE 的一个重要特性是：

```text
总参数 ≫ 激活参数
```

例如：

```text
284B 总参数量
      ↓
每个 token 只激活一小部分 experts
```

因此你不一定需要：

```text
284B × bytes_per_parameter
```

都放在显存里。

相反，你需要：

```text
显存
+ 内存
+ PCIe 带宽
+ GPU 算力
+ expert 局部性/缓存
```

FreeToken 的 `offload` 后端将 experts 保存在主机内存中，并在 GPU 上维护一个 LRU 缓存；缓存未命中时通过 PCIe 流式传输。([GitHub][2])

这是一个非常有趣的架构转变。

---

# 3. 这使 PCIe 成为 AI 基础设施中更重要的部分

这可能是最值得关注的部分。

历史上：

```text
GPU:
  计算
  HBM/显存

CPU:
  编排
```

PCIe 主要被视为 I/O 总线。

FreeToken 实际上是在说：

```text
PCIe = 模型服务的内存结构
```

例如：

```text
内存
 │
 │  根据平台不同约 10-30 GB/s
 │
 ▼
PCIe Gen4/Gen5
 │
 ▼
GPU 显存
 │
 ▼
Tensor cores
```

现在硬件采购的思路开始不同了。

不再只是：

> "这块 GPU 有多少显存？"

你开始问：

```text
显存容量
显存带宽
PCIe 代数
PCIe 通道数
CPU 内存带宽
内存容量
内存带宽
GPU 算力
expert 缓存局部性
```

这是一个 **重大的概念转变**。

---

# 4. 它可能让便宜的二手 GPU 变得更有价值

这对于你一直在关注的硬件类型尤其有趣。

假设你有：

```text
RTX 3090
24GB 显存
```

以及：

```text
128GB DDR4/DDR5
PCIe Gen4 x16
```

你不一定需要因为模型有数千亿参数就去买一块 5000-10000 美元的加速器。

你可以构建：

```text
        128GB 内存
             │
             │ PCIe
             ▼
       RTX 3090 24GB
             │
             ▼
          MoE 模型
```

GPU 变成了 **热执行/缓存层**，而不是整个模型的存储层。

FreeToken 的文档明确描述了这种模型：系统内存可以包含完整的 expert 池，而显存则保存共享/非 expert 权重、KV 状态和最近使用的 experts。([FreeToken Wiki][3])

这意味着：

**二手 GPU + 大量内存 + 好的 PCIe 主板**

变成了一种更有趣的本地 AI 配置。

---

# 5. 但有一个重要的陷阱

这并不会神奇地让：

```text
284B 模型
```

等同于：

```text
24B 模型
```

瓶颈变成了 **带宽**。

假设一次 expert 获取需要：

```text
1 GB
```

而 PCIe 实际给你：

```text
20 GB/s
```

仅理论传输就需要：

```text
1 GB / 20 GB/s
= 50 ms
```

这已经是：

```text
~20 tok/s
```

还没考虑计算、同步、多个 experts、内核等。

所以实际的公式变成了类似：

$$
T_{token}
\approx
\max(
T_{GPU},
T_{CPU},
T_{PCIe}
)
$$

并需要良好的重叠。

这就是为什么 FreeToken 有带宽自适应执行和多个后端：

```text
fused
offload
cpu
hybrid
```

`hybrid` 模式可以通过 PCIe 获取一些 experts，同时在 CPU 上计算其他 experts。([GitHub][2])

---

# 6. 而这正是研究变得真正有趣的地方

FreeToken 不仅仅是：

```text
"CPU 卸载"
```

那是老生常谈。

真正有趣的问题是：

> **模型的每一部分在此时此刻应该位于何处？**

你拥有：

```text
GPU
 ├── 计算
 ├── 显存
 └── 高带宽

CPU
 ├── 计算
 ├── 内存
 └── 大容量

PCIe
 └── 传输
```

运行时动态决定：

```text
expert A → GPU
expert B → 内存
expert C → CPU
expert D → GPU
```

基于：

```text
路由
缓存状态
PCIe 带宽
CPU 性能
GPU 可用性
KV 缓存压力
```

这更接近于 **分布式系统/内存调度**，而不是传统的推理。

---

# 7. 这也改变了“本地 AI”的含义

我认为有三个阶段。

### 阶段 1 — GPU 本地

```text
模型
  ↓
显存
  ↓
GPU
```

示例：

```text
7B
14B
32B
70B
```

取决于量化程度。

---

### 阶段 2 — CPU/GPU 卸载

```text
内存
 ↓
PCIe
 ↓
GPU
```

你可以运行更大的模型，但性能会变得很痛苦。

这是许多现有本地推理系统历史上一直在做的。

---

### 阶段 3 — 异构推理

FreeToken 正在推动：

```text
                 ┌──── GPU
                 │
模型状态 ────────┼──── CPU
                 │
                 ├──── 内存
                 │
                 ├──── PCIe
                 │
                 └──── KV 缓存
```

由运行时决定如何分配计算和状态。

这是一种更具扩展性的架构。

---

# 8. MoE 使这一点尤其强大

我认为这是 FreeToken 时机有趣的最大原因。

行业越来越关注：

```text
MoE
```

因为：

```text
总参数 ↑
激活参数 ↓
```

例如：

```text
模型：

300B 参数

但每个 token：
     ↓
只激活约 20B
```

这几乎完美适用于异构本地推理。

你可以将：

```text
300B
```

分布在：

```text
内存 + 显存
```

但每个 token 只移动/使用：

```text
活跃的 experts
```

FreeToken 支持的模型列表已经包括 DeepSeek-V4-Flash、Qwen3.6/3.5 MoE、GLM-5.2、gpt-oss、Gemma-4 和 MiniMax-M2.5 等模型。([GitHub][2])

所以我认为 **MoE + 量化 + 异构内存** 将是主要的本地推理趋势之一。

---

# 9. 更大的影响：模型规模将持续爆炸

这是一个有趣的反馈循环。

设想行业发现：

```text
300B MoE
```

可以在以下配置上合理运行：

```text
一块工作站 GPU
+
128/256GB 内存
+
PCIe Gen5
```

那么模型设计师就没有太多理由去限制：

```text
总参数数量
```

因为服务不需要：

```text
所有参数都在显存中
```

于是你可以得到：

```text
35B
 ↓
100B
 ↓
300B
 ↓
700B
 ↓
1T+
```

而活跃计算可能仍然小得多。

这创造了一个有趣的未来：

> **“大模型，小活跃模型”成为常态。**

---

# 10. 这也可能降低“消费级 GPU 显存”作为唯一指标的重要性

想象这两台机器：

### 机器 A

```text
GPU:
RTX 5090
32GB 显存

内存:
64GB

PCIe:
Gen4
```

### 机器 B

```text
GPU:
RTX 4090
24GB 显存

内存:
256GB

PCIe:
Gen5 x16
```

对于传统推理：

```text
A > B
```

因为 A 有更多显存。

对于大型 MoE 推理：

```text
B 可能会出人意料地有竞争力
```

因为：

```text
256GB 内存
+
更高的主机容量
+
快速 PCIe
```

可以弥补较小的显存池。

这是硬件经济学的一个重大变化。

---

# 11. 但暂时不要过度高估 FreeToken

有一个非常重要的现实检验。

FreeToken 本身仍然年轻。

仓库发展极快，甚至其自身的 issue 追踪器中也存在性能问题。例如，最近一个报告发现，在 2×3090 DeepSeek-V4-Flash 设置上，自动选择的 `hybrid` 只达到了 **0.67 tok/s**，而强制使用 `offload` 则达到了 **5.58 tok/s**。([GitHub][4])

所以我不会得出以下结论：

> "FreeToken 解决了本地 700B 推理。"

而是：

> **FreeToken 证明了一种不同的服务架构是可行的。**

这才是重要的部分。

---

# 12. 我认为真正的趋势比 FreeToken 更大

我大致将即将到来的本地推理栈排名如下：

```text
                    本地 AI
                       │
        ┌──────────────┼──────────────┐
        │              │              │
       MoE         量化         KV/缓存
        │              │              │
        └──────────────┼──────────────┘
                       │
                  异构内存
                       │
        ┌──────────────┼──────────────┐
        │              │              │
       GPU           CPU           内存
        │              │              │
        └──────────────┼──────────────┘
                       │
                    PCIe/CXL
                       │
                本地 AI 服务器
```

然后：

```text
推测解码
MTP
expert 缓存
前缀缓存
KV 压缩
量化
内核优化
```

都堆叠在上面。

---

# 13. 这创造了一种新型的 AI 工程师

这实际上与你最近学习的内容相关。

有价值的技能将不再是：

> "我了解 vLLM。"

而是变成：

```text
PyTorch
   ↓
CUDA
   ↓
Triton
   ↓
注意力机制
   ↓
MoE
   ↓
量化
   ↓
KV 缓存
   ↓
expert 缓存
   ↓
PCIe
   ↓
CPU/GPU 调度
   ↓
分布式/异构服务
```

你本质上正在成为一名 **模型系统工程师**。

而 FreeToken 是一个非常好的研究项目，因为你能够看到这个边界：

```text
LLM 架构
        ↓
MoE 路由
        ↓
内存放置
        ↓
GPU 内核
        ↓
PCIe 传输
        ↓
调度器
        ↓
服务 API
```

这比仅仅调用推理 API 要深入得多。

---

# 14. 我的预测

我会做出以下押注：

| 趋势                                                         |   我的信心 |
| ------------------------------------------------------------ | ---------: |
| MoE 将变得越来越主导                                         |   **极高** |
| 量化将变得越来越激进                                         |   **极高** |
| 本地推理将变得异构化                                         |   **极高** |
| CPU/内存将成为模型服务的活跃部分                              |     **高** |
| PCIe 带宽将成为重要的 AI 指标                                |     **高** |
| 100B–1T 的开源模型将越来越容易在本地运行                     |     **高** |
| 单块消费级 GPU 服务前沿 MoE 将成为常态                       |     **高** |
| FreeToken 本身成为主导运行时                                  | **低/未知** |
| vLLM/TensorRT-LLM 消失                                       |     **极低** |

最后一点很重要。

**FreeToken 不需要获胜，这套架构就能获胜。**

其他人可以在以下运行时中实现相同的理念：

```text
vLLM
llama.cpp
SGLang
TensorRT-LLM
MLC
新运行时
```

而架构趋势仍然会获胜。

---

## 最重要的收获

我会用一句话总结 FreeToken：

> **FreeToken 是一个早期范例，它将本地 LLM 服务从“把模型塞进显存”转向了“将 GPU 算力、显存、内存、CPU 和互连组合成一个推理系统”。**

我认为 **这是未来 2-5 年本地 AI 的一个真正重要的方向**。

真正有趣的研究问题不是：

```text
"如何让一个 300B 的模型塞进 24GB 的 GPU？"
```

而是：

```text
"在 24GB 显存 + 256GB 内存 + PCIe Gen5 的条件下，
如何调度每一个字节和每一个 expert
以最大化 tokens/秒？"
```

这是一个 **系统问题**，而这正是 CUDA/Triton/MoE/KV 缓存知识开始变得极具价值的地方。

参考资料：

* [FreeToken GitHub 仓库](https://github.com/FlashML-org/FreeToken?utm_source=chatgpt.com)
* [FreeToken 论文——Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](https://arxiv.org/abs/2608.16157?utm_source=chatgpt.com)
* [FreeToken 支持模型和 MoE 后端](https://github.com/FlashML-org/FreeToken/blob/main/docs/models.md?utm_source=chatgpt.com)
* [FreeToken CLI / 服务架构](https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md?utm_source=chatgpt.com)
* [FreeToken 路线图](https://github.com/FlashML-org/FreeToken/issues/79?utm_source=chatgpt.com)

[1]: https://arxiv.org/abs/2608.16157?utm_source=chatgpt.com "FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution"
[2]: https://github.com/FlashML-org/FreeToken/blob/main/docs/models.md?utm_source=chatgpt.com "FreeToken/docs/models.md at main · FlashML-org/FreeToken · GitHub"
[3]: https://www.freetoken.wiki/hardware/FreeToken-vram?utm_source=chatgpt.com "FreeToken vram: Setup Guide for Local MoE Inference - FreeToken Wiki"
[4]: https://github.com/FlashML-org/FreeToken/issues/151?utm_source=chatgpt.com "`ft bench bw` picks `hybrid` on Ampere, but `offload` is 8.3x faster (DeepSeek-V4-Flash, 2x RTX 3090) · Issue #151 · FlashML-org/FreeToken · GitHub"