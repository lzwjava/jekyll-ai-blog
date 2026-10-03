---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI驱动物理基础设施超级周期
translated: true
type: note
---

问题：**a16z最新的“State of Markets”报告对市场有何评价？**

答案：最新的报告是 **“State of Markets II”，发布于2026年9月30日**。它比一月份的报告有趣得多，因为a16z基本上认为 **市场已进入一个更广泛的技术/基础设施超级周期，AI正在将资本从软件拉向物理基础设施**。（[Andreessen Horowitz][1]）

### 核心观点

**1. 技术不再只是一个领域——它正在成为“无所不包的循环”。**

a16z表示，截至2026年8月下旬，技术贡献了 **S&P 500约76%的收益增长**。

他们的论点是，旧的经济周期由实物商品驱动——房屋、汽车、家电——而过去十年则由软件主导。现在，技术已嵌入整个经济中。（[Andreessen Horowitz][1]）

---

**2. 大转变是“比特 → 原子”。**

这可能是对你最重要的部分。

上一个循环：

```text
软件
  ↓
云
  ↓
SaaS
  ↓
开发工具
```

当前循环：

```text
AI模型
   ↓
GPU/ASIC计算
   ↓
内存
   ↓
网络
   ↓
电力
   ↓
数据中心
   ↓
机器人/制造/物理AI
```

a16z认为，在软件占据大部分关注度多年之后，硬件和基础设施正在回归。

他们特别提到：

* 半导体
* GPU/计算
* 内存
* 网络
* 电力/电网
* 机器人技术
* 制造业
* 国防
* 自动驾驶汽车

作为获得异常强劲资本投资的领域。（[Andreessen Horowitz][1]）

这与你的 **二手GPU/GPU维修/小型GPU实验室** 思路直接相关。

---

### 3. “GPU过时”并没有像人们预期的那样发生

这可能是对你的硬件实验最有趣的发现。

传统的论点是：

```text
A100 → H100 → H200 → B200 → 下一代
             ↓
       旧的GPU变得一文不值
```

但a16z表示，实际需求目前正展现出不同的情况。

AI推理需求随着智能成本降低而持续扩展：

```text
更好的模型
     +
更便宜的推理
     ↓
更多的AI使用
     ↓
更多的token
     ↓
更多的计算需求
```

所以 **A100在经济上仍然是有用的**，根据a16z，当他们撰写报告时，A100的租赁价格实际上处于或高于年初水平。（[Andreessen Horowitz][1]）

这基本上是 **Jevons' paradox应用于AI计算**：

> 更便宜的智能 → 戏剧性地更多消费 → 可能更高的总计算需求。

这是一个非常重要的反驳论点，反对简单的 *“新GPU = 旧GPU垃圾”* 观点。

---

### 4. 我们在AI应用方面仍然极为早期

我认为这部分对于如果你正在考虑创办AI咨询业务来说特别重要。

a16z表示：

* 近 **30%的S&P 500公司** 报告了可量化的AI影响
* 但只有约 **2%** 报告了跟踪指标
* 有意义的、大规模的agent部署仍然只占整体使用的一小部分
* 截至2026年4月，仅有约 **2%的美国家庭** 为AI服务付费

所以他们的解释基本上是：

```text
计算需求：       ██████████
AI能力：        ██████████
实际深度应用： ██
```

基础设施建设已经非常庞大——**在成熟的AI应用到来之前**。（[Andreessen Horowitz][1]）

---

### 5. SaaS没有死——但它必须证明自己

a16z反驳了2026年的 **“SaaSpocalypse”** 说法。

他们的数据：

```text
2022年：
高增长
低盈利能力

2026年：
约75%盈利
约30%增长率>20%
```

所以问题不仅仅是：

> AI杀死了软件。

更准确的是：

> 停止增长的软件公司不再配得上他们在ZIRP时期获得的巨大增长倍数。

快速增长的软件公司仍然可以获得高估值；只是数量更少了。a16z称这是 **“prove it”，而不是“pocalypse”**。（[Andreessen Horowitz][1]）

---

## 6. a16z认为下一步扩展将去向何方

他们的前瞻性论点：

```text
AI
 │
 ├── Enterprise
 │     └── 更深入的应用
 │
 ├── Consumer
 │     └── 更深入的应用
 │
 ├── Robotics
 │
 ├── Biotech
 │
 ├── Healthcare
 │
 └── Autonomous driving
```

换句话说，**AI不仅仅是取代SaaS的功能**。

他们的论点是，AI扩展了软件+机器+物理基础设施的总可涉及面。（[Andreessen Horowitz][1]）

---

# 我会关注的部分，针对你的情况

我会将这个报告的世界观总结为：

```text
过去：
互联网 → 软件 → SaaS

2026+：
AI
 │
 ├── models
 ├── agents
 ├── software
 ├── GPUs
 ├── datacenters
 ├── networking
 ├── electricity
 ├── robots
 └── physical economy
```

而这使得你看似不相关的兴趣——**LLMs + agents + GPU hardware + GPU repair + cheap compute + software consultancy**——实际上契合了一个更大的技术周期。

有趣的机会不一定就是 *“build another SaaS。”*

它可能更接近于：

```text
cheap compute
      +
open models
      +
coding agents
      +
human engineering
      ↓
AI-native software production
      ↓
clients
```

而物理层面则是：

```text
used GPUs
   ↓
repair / testing
   ↓
cheap compute
   ↓
local inference / training
   ↓
AI services
```

而a16z的最新报告本质上是在说 **物理计算/基础设施方面正变得越来越重要，而不是越来越不重要。**

还有一份独立的a16z **100-trillion-token OpenRouter研究** 更贴近你实际的LLM/agent工作：它发现向推理、多轮工作流、工具使用和agentic inference的迅速转变。（[Andreessen Horowitz][2]）

[a16z — State of Markets II](https://a16z.com/state-of-markets-ii/?utm_source=chatgpt.com)
[a16z — State of AI: 100 Trillion Token Study](https://a16z.com/state-of-ai/?utm_source=chatgpt.com)

[1]: https://a16z.com/state-of-markets-ii/?utm_source=chatgpt.com "State of Markets II | Andreessen Horowitz"
[2]: https://a16z.com/state-of-ai/?utm_source=chatgpt.com "State of AI: An Empirical 100 Trillion Token Study with OpenRouter | Andreessen Horowitz"
