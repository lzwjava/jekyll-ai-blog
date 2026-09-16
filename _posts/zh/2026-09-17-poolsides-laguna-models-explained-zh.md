---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Poolside的Laguna模型详解
translated: true
type: note
---

问题：**请介绍一下 Poolside，并解释其模型——特别是 Laguna 系列以及通过 OpenRouter 暴露的六个模型。**

答案：

## 1. 什么是 Poolside？

![Image](https://images.openai.com/static-rsc-4/hD3ea6ogsqShzK5Hr1tEM6OSz74qflDwGaQu89OWACFzApspKGrWZag5SM3ngPifYCv-qX4xWd8N3FXh1mhfFRUgayp-GKFFAU7cx63LTBe8qaXkBzGRhLf3KFpOW1v-tFEcz19ktTNsJhzsrGHkNwC63NR_bKz3X2tLhmfBPvZEZG9FZTlx50OrPMibylSH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5SOWVPq0eQDISVMbulCYzUPDwV7loLd606gIZf8OXYeeTAQtNVOwePf6pFJRfNrRc1hVlNTqAVBQIDu3d-SSsOKmnm6dS5jYutsmeCcDY6OQ3RIvfZOqdqdC8mhiggnrOggC2nO6c0AA_azsXDE_AQlaVnTeP2WulicnWw68Bhf04g0KERxaclnRN1h8YU_i?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/rsWvNIdAxUduXGkjdHMzpwHImJkLKEk5mq0MnK93EQxOnL-SwE7sseLbWX5yFVEaOmPP2oe3sgbjPOA6e7RzpwQjjGwLyRN5MLm7darWdCIOy49WYvigA93fVMEUQQVUBrGLl9S-tzuzk-8u35t_wv9R-WyevEfbtr9i8u5kkvDAYZ43TYGLAnXsptlSHprj?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_k945JzwC-EUxJXdKEH0SjRnvTm0xyl6UdR3p1H0UVJq4njJsC0BrEJvuGIqgg083RtXUvnyYD6MF34otGazwE7H9l5Tr4M5039I1Free4z76kRlXyBsM11WWc3MOojG4bsWLgb5cQKkUOOnrOktxoplmhObQgeFuUivl6efcYfodJ-lFpiUsADswBZ-gsAz?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qy54kQT6hcRpJvf9XPvxz-UuIJT3PcAobgjD4U8NOzu49RpAD03YyM7uBrifEKqBI2dg9ezGF2okAq8yn4_n85xUL1-zD2_8EuCYnPiyDxJtTPXWuxGDQKNtf2OpAKIVQZaaHI86rMZS6Gt3jmLwnEnkhZsVgEC50bxwj4eLagCy9o_tSkkHajO8Zg1b-u3j?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/NO4Yt8WygaXYdZ2VKtq-Wgabl6nWBp62VDODbA4iVI4bGpKd9ZiRY8sJM4fgkKyqKvtV28r-hjSRuMUWRL8Z8YTCuytHnuVKo8b0BTREpYLXr7LjJwTotxgCOlf18vWoFVPj0gI2cHvSE-vnljTx326qB09vdshW2N3QoOiTNtSVo56IXZCXo0Vp5KZMZSRa?purpose=fullsize)

Poolside 是一家 AI 公司，由前 GitHub CTO **Jason Warner** 和前 Athenian 创始人/CEO **Eiso Kant** 于 2023 年创立。他们的理念异常专注：

> **将软件工程作为通往日益通用的 AI 能力的路径。**

Poolside 并非从通用聊天机器人开始再添加编码能力，而是专门围绕**软件工程智能体**构建基础模型。

该公司在 2024 年 10 月完成了 **5 亿美元的 B 轮融资**，据报道当时总融资额约为 **6.26 亿美元**，投资者包括 Bain Capital Ventures、Nvidia、eBay Ventures、Felicis 和 Redpoint。（[TechCrunch][1]）

对于您而言，其策略架构值得关注：

```text
                         Poolside
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Foundation models           Agent runtime
              │                           │
          Laguna family                  pool
              │                           │
      ┌───────┼────────┐                  │
      │       │        │                  │
     S.2.1   M.1     XS.2.1        long-horizon coding
      │       │        │
      └───────┴────────┘
              │
       code + terminal + tools
              │
        RL from execution
```

Poolside 明确表示其模型是**从头开始**训练的，使用自己的数据、基础设施和强化学习。其模型是在智能体框架内训练的，而不仅仅是优化代码的下一词元预测。（[Poolside][2]）

这个区别很重要。

---

# 2. 核心理念：将编码作为智能体环境

Poolside 实际上优化的目标并非：

```text
prompt → code completion
```

而是更接近：

```text
goal
 ↓
reason
 ↓
inspect repository
 ↓
modify files
 ↓
run compiler/tests
 ↓
observe failure
 ↓
reason again
 ↓
modify
 ↓
repeat
```

这也是为什么他们的基准测试高度偏向智能体：

* Terminal-Bench
* SWE-bench
* DeepSWE
* SWE-bench Multilingual
* SWE-bench Pro
* Toolathlon

Poolside 表示，其 Laguna 模型是**在其智能体框架内**使用强化学习训练的，评估时使用多达数百次交互步骤，而非将编码视为单次补全。（[Poolside][2]）

对于智能体构建者来说，这可能是理解 Poolside 最重要的一点。

---

# 3. OpenRouter 上的六个模型

截至 2026 年 9 月，OpenRouter 提供了六个 Poolside 模型：

| 模型                  | 参数 | 激活参数 |  上下文 |       输入 / 输出价格 | 主要特点                 |
| ---------------------- | -----: | -----: | --------: | -------------------: | ------------------------- |
| **Laguna S 2.1**       |   118B |     8B | **1.05M** | $0.09 / $0.18 per 1M | 旗舰模型                  |
| **Laguna S 2.1 free**  |   118B |     8B |      262K |                 Free | 同一模型，免费端点 |
| **Laguna XS 2.1**      |    33B |     3B |      262K | $0.06 / $0.12 per 1M | 快速/便宜              |
| **Laguna XS 2.1 free** |    33B |     3B |      262K |                 Free | 免费 XS                   |
| **Laguna XS.2**        |    33B |     3B |      262K |                    — | 上一代 XS    |
| **Laguna M.1**         |   225B |    23B |      262K |                    — | 上一代旗舰         |

OpenRouter 目前列出了这六个模型及其上下文和定价信息。（[OpenRouter][3]）

一个微妙之处：**“118B”并不意味着每个词元执行 118B 参数。**

Laguna S 2.1 是 MoE：

```text
118B total parameters
       │
       ├── expert 1
       ├── expert 2
       ├── expert 3
       ├── ...
       └── expert N
             │
          router
             │
       ~8B activated
             │
           token
```

因此推理计算量更接近约 8B 激活参数，而非密集的 118B 模型。

同样：

```text
Laguna XS 2.1
33B total
3B active
```

根据其模型文档，Poolside 在 **30T tokens** 上训练了 S 2.1，在 **15T tokens** 上训练了 XS 2.1。（[Poolside][2]）

---

# 4. Laguna S 2.1

这是我最为关注的模型。

**架构**

```text
118B total
8B active
MoE
30T training tokens
1,048,576 context
```

Poolside 将其描述为在**智能体编码和长周期任务**方面最强的模型。（[Poolside][2]）

OpenRouter 目前报告：

```text
Input:  $0.09 / 1M tokens
Output: $0.18 / 1M tokens
Context: 1.05M
```

并且报告：

```text
Terminal-Bench 2.1    70.2%
DeepSWE                40.4%
```

该模型。（[OpenRouter][3]）

有趣之处不仅仅是基准测试分数。

而是这个组合：

```text
118B total
8B active
+
1M context
+
agentic coding
+
open weights
+
$0.09/M input
```

这在模型设计空间中相当罕见。

---

# 5. Laguna XS 2.1

这可以说是更有趣的工程模型。

```text
33B total
3B active
256K context
up to 32K output
```

Poolside 称其为**最轻量、最快的智能体编码模型**。（[Poolside][4]）

该模型于 2026 年 7 月 2 日发布，相较于 XS.2 有显著提升，特别是在多语言软件工程方面。Poolside 报告 SWE-bench Multilingual 提升了 **5.4 个百分点，达到 63.1%**。（[Poolside][4]）

付费的 OpenRouter 端点目前：

```text
input:       $0.06 / 1M
output:      $0.12 / 1M
cache-read:  $0.03 / 1M
```

上下文窗口为 262,144 个词元，最大补全为 32,768 个词元。（[OpenRouter][5]）

所以概念上：

```text
                 Laguna S 2.1
                      │
              maximum capability
                      │
                 118B / 8B
                      │
                   1M ctx
                      │
                      ▼
             complex long-horizon
                  agents


                 Laguna XS 2.1
                      │
                 efficiency
                      │
                  33B / 3B
                      │
                  256K ctx
                      │
                      ▼
             cheap / fast agents
```

这是一个非常合理的模型系列。

---

# 6. M.1 和 XS.2 怎么了？

这些是上一代产品。

### Laguna M.1

```text
225B total
23B active
256K context
```

它是 Poolside 在 Laguna 系列中的原始旗舰模型。Poolside 于 2026 年 4 月发布。（[Poolside][6]）

### Laguna XS.2

```text
33B total
3B active
256K context
```

这是原始的较小模型。

它特别引人注目，因为 Poolside 在 **Apache 2.0** 许可下公开了其权重。（[Poolside][6]）

XS 2.1 本质上是该系列的下一次迭代，Poolside 转向了 **OpenMDW-1.1** 许可。（[Poolside][7]）

因此演变大致如下：

```text
             2026

       M.1 ────────────────┐
       225B / 23B          │
                           │
                           ▼
                    Laguna S 2.1
                    118B / 8B
                    1M context


       XS.2 ───────────────┐
       33B / 3B            │
                           ▼
                    Laguna XS 2.1
                    33B / 3B
                    256K context
```

真正有趣的优化在于：**S 2.1 的总参数比 M.1 小，却显然成为了 Poolside 的旗舰**。

这说明 Poolside 试图通过架构 + 数据 + RL 来获得更高的单位推理算力能力，而非简单地扩大参数量。

---

# 7. 为什么 Poolside 在技术上引人注目

我关注三个方面。

### ① RL 是核心，而非点缀

他们的公开描述基本上是：

```text
pretraining
    ↓
synthetic/code data
    ↓
agent environment
    ↓
execute code
    ↓
observe outcome
    ↓
RL
    ↓
better agent trajectories
```

这与以下优化目标有根本区别：

```text
code corpus → next-token loss
```

Poolside 明确将大规模代码执行的强化学习描述为其 Model Factory 的一部分。（[Poolside][2]）

---

### ② MoE 带来了有趣的成本曲线

比较：

```text
Laguna S 2.1
118B total → 8B active

Laguna XS 2.1
33B total → 3B active
```

该模型具有较大的潜在容量，但每个词元仅激活一小部分子集。

这对于编码智能体尤其有吸引力，因为智能体可能在长轨迹中生成了**成千上万个词元**。

推理成本至关重要。

---

### ③ 他们同时构建模型和智能体运行时

Poolside 的 `pool` 运行时不仅仅是 LLM 的外壳。

他们自己的描述是：

```text
Laguna
  +
agent harness
  +
terminal
  +
file operations
  +
execution feedback
  +
RL
```

他们说 Laguna 模型在 `pool`（他们自己的编码智能体环境）中表现最佳，尽管这些模型也可以通过兼容 OpenAI 的 API 和其他 ACP 客户端使用。（[Poolside][2]）

这类似于我们看到的更广泛的转变：

```text
LLM company
```

走向：

```text
model
+
runtime
+
tools
+
environment
+
RL
+
agent product
```

---

# 8. OpenRouter 让实验变得极其简单

您可以使用相同的 OpenAI SDK 并切换模型。

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="<PLACEHOLDER>",
)

r = client.chat.completions.create(
    model="poolside/laguna-s-2.1",
    messages=[
        {
            "role": "user",
            "content": "Inspect this repository and identify the race conditions."
        }
    ],
)

print(r.choices[0].message.content)
```

然后使用以下模型对同一智能体进行基准测试：

```python
models = [
    "poolside/laguna-s-2.1",
    "poolside/laguna-s-2.1:free",
    "poolside/laguna-xs-2.1",
    "poolside/laguna-xs-2.1:free",
]
```

OpenRouter 在同一个兼容 OpenAI 的 API 后面公开了所有这些模型。（[OpenRouter][3]）

免费端点的一个注意事项：OpenRouter 明确指出，**Poolside 可能会使用免费使用的输入和输出来训练/改进其模型**。（[OpenRouter][8]）

---

# 9. 我对 Poolside 的心智模型

如果我把这家公司压缩成一个图示：

```text
                    Poolside
                       │
          "AGI through software"
                       │
                       ▼
              Software agents
                       │
             ┌─────────┴─────────┐
             │                   │
         Foundation           Environment
           models                 │
             │                 pool / ACP
       ┌─────┴─────┐              │
       │           │              │
   Laguna S      Laguna XS        │
   118B/8B       33B/3B           │
       │           │              │
       └─────┬─────┘              │
             │                    │
             └────────┬───────────┘
                      │
                 code execution
                      │
                      ▼
                      RL
                      │
                      └──────→ better agents
```

这就是为什么我不会简单地将 Poolside 归类为“另一家开源权重 LLM 公司”。

他们更有趣的赌注是：

> **软件工程是一个足够丰富的环境，可以训练出能力越来越强的推理智能体。**

Laguna 模型是该赌注的模型组成部分。

截至目前，**S 2.1 是拥有 1M 上下文的旗舰模型**，而 **XS 2.1 是针对高吞吐量/本地/快速智能体编码的紧凑型 33B/3B 模型**。OpenRouter 为您提供了一种非常便宜的方式来实验性地比较两者。（[Poolside][2]）

参考文献：

* [Poolside Models](https://www.poolside.ai/models?utm_source=chatgpt.com)
* [Poolside — Laguna XS 2.1 announcement](https://www.poolside.ai/blog/introducing-laguna-xs-2-1?utm_source=chatgpt.com)
* [OpenRouter — Poolside models](https://openrouter.ai/poolside?utm_source=chatgpt.com)
* [OpenRouter — Laguna XS 2.1](https://openrouter.ai/poolside/laguna-xs-2.1-20260625?utm_source=chatgpt.com)
* [Poolside — $500M fundraise](https://www.poolside.ai/blog/announcing-our-500-million-fundraise-to-make-progress-towards-agi?utm_source=chatgpt.com)
* [TechCrunch — Poolside $500M funding](https://techcrunch.com/2024/10/02/ai-coding-startup-poolside-raises-500m-from-ebay-nvidia-and-others/?utm_source=chatgpt.com)

我还可以构建一个 **Poolside vs DeepSeek vs Qwen vs GLM vs Kimi 编码智能体架构对比**，包括激活参数、训练词元、RL 设置、上下文和推理经济性。

[1]: https://techcrunch.com/2024/10/02/ai-coding-startup-poolside-raises-500m-from-ebay-nvidia-and-others/?utm_source=chatgpt.com "AI coding startup Poolside raises $500M from eBay, Nvidia, and others | TechCrunch"
[2]: https://www.poolside.ai/models?utm_source=chatgpt.com "Models — Poolside"
[3]: https://openrouter.ai/poolside "poolside API and Models | OpenRouter"
[4]: https://www.poolside.ai/blog/introducing-laguna-xs-2-1?utm_source=chatgpt.com "Introducing Laguna XS 2.1 — Poolside"
[5]: https://openrouter.ai/poolside/laguna-xs-2.1-20260625?utm_source=chatgpt.com "Laguna XS 2.1 - API Pricing & Providers | OpenRouter"
[6]: https://poolside.ai/blog/introducing-laguna-xs2-m1?utm_source=chatgpt.com "Introducing Laguna XS.2 and Laguna M.1 — Poolside"
[7]: https://poolside.ai/blog/introducing-laguna-xs-2-1?utm_source=chatgpt.com "Introducing Laguna XS 2.1 — Poolside"
[8]: https://openrouter.ai/poolside/laguna-s-2.1-20260720%3Afree?utm_source=chatgpt.com "Laguna S 2.1 (free) - API Pricing & Providers | OpenRouter"