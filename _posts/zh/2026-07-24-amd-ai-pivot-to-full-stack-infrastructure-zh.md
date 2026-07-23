---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD AI 转向全栈基础设施
translated: true
type: note
---

Question: What did Lisa Su share in the recent AMD AI meeting?

Answer:

在 **AMD Advancing AI 2026** 上，Lisa Su 传达的核心信息是：AMD 正从“GPU 替代品”转型为一家直接与 NVIDIA 竞争的全栈 AI 基础设施公司。主题演讲聚焦于 **AI 工厂、开放生态系统和扩展 AI 计算**。([AMD][1])

要点如下：

## 1. AI 正从训练转向大规模推理

Lisa Su 强调，下一波 AI 浪潮不仅关乎训练巨型模型。更大的机会在于：

* billions of AI agents
* continuous inference workloads
* enterprise AI factories
* sovereign AI infrastructure

这意味着：

```
Old AI:
GPU cluster -> train model -> deploy

New AI:
AI factory -> train + fine-tune + serve millions of agents
```

因此 AMD 瞄准了整个堆栈：

```
EPYC CPU
   +
Instinct GPU
   +
Networking
   +
ROCm software
   +
Rack-scale systems
```

([Barron's][2])

---

## 2. Helios：AMD 对 NVIDIA GB200/GB300 级别系统的回应

最大的消息是 **Helios**，AMD 的下一代 AI 机架系统。

其思路是：

不再只销售 GPU：

```
NVIDIA:
B200 / GB200
        ↓
NVLink
        ↓
AI rack
```

AMD 想要：

```
MI455X
  +
Venice EPYC CPU
  +
AMD networking
  +
ROCm
  ↓
Helios AI rack
```

AMD 表示 Helios 已进入生产阶段，预计于 2026 年 Q3 出货。([Reuters][3])

这在战略上十分重要，因为超大规模客户越来越多地购买 **系统**，而非单独的加速器。

---

## 3. 开放生态系统 vs NVIDIA CUDA 锁定

Lisa Su 的长期观点：

> AI 不应由单一的专有堆栈控制。

AMD 正在推动：

```
CUDA ecosystem
      vs
ROCm ecosystem
```

赌注在于：

* 客户希望有多家供应商
* 开放软件降低成本
* AI 基础设施应当可移植

ROCm 成为 AMD 的 CUDA 等价物。

对于开发者而言，问题在于：

```
Can PyTorch model
run efficiently on AMD GPU?
```

而非：

```
Can AMD make a faster chip?
```

因为没有软件，硬件毫无用处。

---

## 4. MI450 / MI455X 代

AMD 展示了其下一代 Instinct 加速器代。

方向：

* 更多内存
* 更高带宽
* 更好的横向扩展
* 机架级优化

对于 LLM 来说，这一点很重要，因为现代瓶颈往往是：

```
not FLOPS

but:

VRAM capacity
HBM bandwidth
interconnect bandwidth
power efficiency
```

一个 200B 参数模型更关心的是：

```
Can I fit KV cache?
Can I serve 10k users?
Can I scale inference?
```

而非峰值 TFLOPS。

---

## 5. 大客户验证

AMD 宣布/提到了主要 AI 客户和合作伙伴，包括 OpenAI、Microsoft、Meta 等。([Reuters][3])

OpenAI 的合作尤其重要，因为它表明 AMD 正在成为真正的 AI 计算替代供应商，而不仅仅是第二供应商。([Reuters][3])

---

## 我从工程师角度的解读

重要的转变是：

### 2023-2025：

```
AI = NVIDIA CUDA + GPUs
```

### 2026+：

```
AI = compute infrastructure

      silicon
        |
      memory
        |
    networking
        |
    compiler
        |
    runtime
        |
    models
        |
    agents
```

AMD 试图赢得 **基础设施层**。

对于运行 LLM 训练/推理的人来说，实际后果是：

以前：

```
Need AI cluster?
Buy NVIDIA.
```

未来：

```
Need AI cluster?

Compare:
- NVIDIA CUDA stack
- AMD ROCm stack
- Google TPU
- custom ASICs
```

竞争正从芯片转向完整的 AI 工厂。([Barron's][2])

参考文献：

* [AMD Advancing AI 2026 Keynote](https://www.amd.com/en/corporate/events/advancing-ai/keynote.html?utm_source=chatgpt.com)
* [AMD Advancing AI 2026 Event Overview](https://www.amd.com/en/corporate/events/advancing-ai.html?utm_source=chatgpt.com)
* [AMD's Helios AI server announcement coverage](https://www.reuters.com/business/amd-expected-launch-next-generation-ai-infrastructure-challenge-nvidia-2026-07-23/?utm_source=chatgpt.com)

[1]: https://www.amd.com/en/corporate/events/advancing-ai/keynote.html?utm_source=chatgpt.com "AMD Advancing AI 2026 Keynote"
[2]: https://www.barrons.com/articles/amd-nvidia-ai-data-center-chips-ea7aac0d?utm_source=chatgpt.com "An Emboldened AMD Is Taking Direct Aim at Nvidia"
[3]: https://www.reuters.com/business/amd-expected-launch-next-generation-ai-infrastructure-challenge-nvidia-2026-07-23/?utm_source=chatgpt.com "AMD says its newest AI server is in full production, will ship in months"