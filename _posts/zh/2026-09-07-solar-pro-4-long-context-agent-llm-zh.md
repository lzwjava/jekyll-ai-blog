---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Solar Pro 4: 长上下文智能体大语言模型'
translated: true
type: note
---

问题：**什么是 Upstage Solar Pro 4，它为什么值得关注？**

答案：

Upstage 的 **Solar Pro 4 (SP4)** 是一款闭源大型语言模型，于 2026 年 8 月发布。其亮点并非仅仅“又一个前沿模型”——它明确针对 **长周期智能体任务** 进行了优化：读取大量上下文 → 调用工具 → 对中间结果进行推理 → 生成最终产物。([Upstage AI][1])

### 1. 关键规格

|                   |           Solar Pro 4 |
| ----------------- | --------------------: |
| 上下文长度        |    **524,288 tokens** |
| 最大输出          |    **131,072 tokens** |
| 输入价格          | **$0.03 / 1M tokens** |
| 输出价格          | **$0.12 / 1M tokens** |
| 缓存输入价格      |       **$0.006 / 1M** |
| 推理能力          |                   支持 |
| 工具调用          |                   支持 |
| 结构化输出        |                   支持 |
| 输入模态          |                   文本 |
| 发布时间          |          2026 年 8 月 10 日 |

524K 这个数字尤其有趣。你可以将 **一个大型代码库或数百页文档** 放进一个上下文窗口中，而无需自行进行激进的分块或 RAG。([OpenRouter][2])

而且价格 *极其* 低廉：

```text
1M 输入  = $0.03
1M 输出 = $0.12

10M 输入 + 2M 输出
= 10 × $0.03 + 2 × $0.12
= $0.54
```

对于需要大量模型调用的智能体来说，这格外有吸引力。

---

### 2. 重要之处：这是一个 **智能体模型**

Upstage 的定位非常明确：

> 不要仅仅回答问题。**完成工作。**

例如：

```text
20 份文档
      │
      ▼
┌───────────────┐
│ Solar Pro 4   │
│               │
│ 推理          │
│ 检查          │
│ 调用工具      │
│ 验证          │
└───────┬───────┘
        │
        ├── Excel
        ├── 报告
        └── PowerPoint
```

Upstage 展示了一个工作流：SP4 阅读一份策略文档加六份市场数据文件，筛选十个候选地点，然后生成 Excel 工作簿、报告和幻灯片演示。([Upstage AI][1])

这与基准测试不同：

```text
提示 → 回答
```

他们瞄准的是：

```text
目标
 ↓
计划
 ↓
读取上下文
 ↓
工具调用
 ↓
观察结果
 ↓
推理
 ↓
工具调用
 ↓
验证
 ↓
交付物
```

这更接近于你正在用 CLI 智能体所做的事情。

---

### 3. 其基准测试表现值得关注

Upstage 报告数据：

* **Terminal-Bench v2.1: 57**
* **τ³-Banking: 23**
* **AA-LCR 长上下文: 71**

对我而言重要的是 **AA-LCR = 71**，因为它衡量的是跨约 10 万 token 文档的推理能力。Upstage 表示这是 SP4 表现尤为出色的领域。([Upstage AI][1])

其更广泛的 Artificial Analysis 评分报告为 **42**，使其处于一般前沿模型的水平，同时价格却比典型的前沿 API 低廉得多。([Upstage AI][3])

因此，我会将其特点概括为：

```text
                 智能水平
                      ↑
                      │       前沿模型
                      │
                      │   Solar Pro 4
                      │
                      │
                      │
                      └──────────────────→
                         成本效益
```

未必是 **最聪明的模型**，但很可能是一款 **$/完成智能体任务** 表现极佳的模型。

---

### 4. 524K 上下文实际上很有用

例如，假设你的编码智能体包含：

```text
系统提示          10K
代码仓库              80K
README                  10K
问题历史记录           20K
工具结果              50K
之前的对话            30K
测试                   20K
────────────────────────────
总计                  220K
```

你可以将几乎所有内容保留在一个上下文中：

```python
messages = [
    系统提示,
    仓库上下文,
    问题,
    对话,
    工具结果,
]
```

而无需频繁进行：

```text
检索 → 摘要 → 检索 → 摘要
```

这可以成为 **智能体可靠性的重大优势**，因为每次摘要都会导致信息损失。

---

### 5. 价格使其对你的智能体尤其具有吸引力

OpenRouter 当前报价：

```text
Solar Pro 4

输入:       $0.03 / 1M
缓存:      $0.006 / 1M
输出:      $0.12 / 1M
```

([OpenRouter][4])

假设你的智能体执行：

```text
100 次调用
平均上下文: 100K
平均输出:   5K
```

那么大约：

```text
输入  = 100 × 100K = 10M tokens
输出 = 100 ×   5K = 0.5M tokens

成本
= 10 × $0.03
+ 0.5 × $0.12
= $0.36
```

即使实际工作量高出数倍，成本仍然只是 **几美元而非几十或几百美元**。

这就是为什么我认为 SP4 作为 **智能体后端** 比作为 ChatGPT 替代品更有趣。

---

### 6. 它也兼容 OpenAI

这对你的技术栈很友好。

OpenRouter 暴露了：

```text
model = "upstage/solar-pro4"
```

并支持工具/函数调用和结构化输出。([OpenRouter][2])

因此，现有的 OpenAI 风格智能体基本上可以做到：

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="..."
)

response = client.chat.completions.create(
    model="upstage/solar-pro4",
    messages=messages,
    tools=tools,
)
```

该模型也支持推理，因此你可以将其用作使用工具的循环中的“大脑”，而不仅仅是文本生成器。([Pi][5])

---

### 7. 我实际会在哪些地方使用它

针对你这类工作，我会在以下方面进行测试：

**① 编码智能体**

```text
代码仓库
 ↓
Solar Pro 4
 ↓
bash
 ↓
pytest
 ↓
检查错误
 ↓
编辑
 ↓
pytest
 ↓
提交
```

**② 大型文档智能体**

```text
10 × 50 页 PDF
        ↓
     SP4
        ↓
跨文档推理
        ↓
结构化答案
```

**③ 研究智能体**

```text
搜索
 ↓
100 份文档
 ↓
提取证据
 ↓
交叉验证
 ↓
撰写报告
```

**④ 办公自动化**

```text
CSV + PDF + 策略
       ↓
    SP4 智能体
       ↓
Excel + 报告 + PPT
```

这些正是 Upstage 声称已优化的任务类型。([Upstage AI][1])

---

### 8. 一个重要区别：Solar Pro 4 ≠ Solar Pro 3

不要混淆。

Solar Pro 3 是一个 **102B 总参数量 / 12B 激活参数的 MoE** 模型。([OpenRouter][4])

Solar Pro 4 的定位更侧重于 **智能体行为 + 长上下文 + 可靠性**，Upstage 并未简单将其呈现为“更大的 Solar Pro 3”。

因此，我建议这样理解：

```text
Solar Pro 3
    ↓
高效通用 LLM / MoE

Solar Pro 4
    ↓
生产级智能体模型
    ├── 长上下文
    ├── 推理
    ├── 工具
    ├── 结构化输出
    └── 文档工作流
```

### 我的看法

**Solar Pro 4 是目前最有趣的“廉价智能体大脑”模型之一。**

组合很不寻常：

```text
524K 上下文
+
推理能力
+
工具调用
+
结构化输出
+
$0.03/M 输入
+
$0.12/M 输出
```

真正的问题不是 *“SP4 比 GPT/Claude/Gemini 更聪明吗？”*

我会测试：

> **成功完成一个真实智能体任务的成本是多少？**

这才是对 `ww`、`iclaw` 或任何生产级编码/研究智能体而言重要的指标。

[Upstage 的 Solar Pro 4 公告](https://www.upstage.ai/blog/en/solar-pro-4?utm_source=chatgpt.com)
[OpenRouter 上的 Solar Pro 4](https://openrouter.ai/upstage/solar-pro4?utm_source=chatgpt.com)

我还可以设计一个 **Solar Pro 4 与 Qwen / Claude / GPT 的编码智能体对比测试**，使用相同的代码仓库和工具循环，这能比排行榜数字告诉你更多信息。

[1]: https://www.upstage.ai/blog/en/solar-pro-4?utm_source=chatgpt.com "Solar Pro 4: The Agentic Model That Finishes the Job"
[2]: https://openrouter.ai/upstage/solar-pro4?view=api&utm_source=chatgpt.com "Solar Pro 4 - API Pricing & Benchmarks | OpenRouter"
[3]: https://www.upstage.ai/news/upstage-ai-unveils-solar-pro-4-scoring-42-on-artificial-analysis-index-to-rank?utm_source=chatgpt.com "Upstage AI Unveils Solar Pro 4, Scoring 42 on Artificial Analysis Index to Rank Among Global Frontier Models"
[4]: https://openrouter.ai/provider/upstage?utm_source=chatgpt.com "Upstage | OpenRouter"
[5]: https://pi.dev/models/openrouter/upstage-solar-pro4?utm_source=chatgpt.com "Upstage: Solar Pro 4 · Models · Pi"