---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Citadel的自我优化研究循环
translated: true
type: note
---

问题：**Ken Griffin / Citadel 最近提到的“自我改进的交易机器”是什么？**

回答：我认为你指的是 Griffin 在 2026 年 Goldman Sachs 采访中描述的 **agentic AI + 量化研究循环**。他并没有从字面上称这个系统为“自我改进的交易机器”，但这是对他所描述想法的一个合理概括。

有趣的是，**Citadel 并不是简单地使用 LLM 来预测股票价格**。

### 其架构更接近于这样

```text
                    ┌─────────────────────┐
                    │   Market / Papers   │
                    │   Data / Research   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Research Agent    │
                    │                     │
                    │ hypothesize         │
                    │ code                │
                    │ backtest            │
                    │ analyze              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Evaluator         │
                    │                     │
                    │ OOS tests           │
                    │ risk                │
                    │ costs               │
                    │ statistical tests  │
                    └──────────┬──────────┘
                               │
                         validated result
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Memory / Dataset  │
                    │                     │
                    │ what worked         │
                    │ what failed         │
                    │ under what regime   │
                    └──────────┬──────────┘
                               │
                               └──────► next hypothesis
```

**自我改进体现在研究循环中**，而不一定在神经网络权重里。

Griffin 表示，Citadel 构建了一个能够读取金融研究论文、**复现其方法论、验证结果，并测试该结果在原始样本之外的数据上是否仍然成立**的智能体。传统上需要硕士/博士研究员团队花 **6-8 周** 完成的工作，据报道现在可以在约 **2-3 小时** 内完成。([Goldman Sachs][1])

这比下面这样的系统有趣得多：

```python
prediction = model.predict(market_data)
```

它更像是：

```python
while True:
    hypothesis = researcher.propose(
        data=data,
        previous_results=memory
    )

    implementation = researcher.implement(hypothesis)

    result = evaluator.run(
        implementation,
        train=train,
        validation=validation,
        test=test,
        transaction_costs=costs
    )

    memory.append({
        "hypothesis": hypothesis,
        "implementation": implementation,
        "result": result,
    })
```

然后下一个研究员会获得累积的证据。

### 而 Citadel 早就开始做非 LLM 版本了

这是容易被忽视的部分。

Griffin 表示 Citadel 使用**机器学习约 10 年**，包括 TensorFlow。他描述过工程师如何极其迅速地采用 TensorFlow，并将其投入美国股票报价的生产环境。([Bishop Rock Capital][2])

在 2026 年的讨论中，他特别提到基于 transformer 的新型模型提升了 Citadel Securities **定价和风险管理**的能力。([Goldman Sachs][1])

所以演变过程大致是：

```text
2000s
  │
  ├── human-designed quantitative models
  │
  ▼
2010s
  │
  ├── ML models
  ├── automated feature discovery
  ├── automated pricing
  └── automated risk models
  │
  ▼
2020s
  │
  ├── transformers
  ├── foundation models
  └── LLM-assisted research
  │
  ▼
2026
  │
  ├── agents
  ├── code generation
  ├── autonomous experiment execution
  ├── automated statistical validation
  └── persistent research feedback loop
```

**而最后一步才是关键**。

---

## 为什么这确实是“自我改进的”

假设你给机器：

```text
Universe: US equities
Data: 20 years
Objective: predict 5-minute returns
```

一个普通的 ML 流程可能是：

```text
data → features → model → prediction → trading
```

而 agentic 研究系统可以这样做：

```text
          ┌──────────────┐
          │  hypothesis  │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ write code   │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ backtest     │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ diagnose     │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ modify idea  │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ OOS test     │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ record result│
          └──────┬───────┘
                 │
                 └──────────→ next experiment
```

**优化目标不仅仅是模型损失**。

可以是类似：

$$
J =
\text{Sharpe}
-\lambda_1\text{Turnover}
-\lambda_2\text{Drawdown}
-\lambda_3\text{Costs}
-\lambda_4\text{Complexity}
$$

智能体搜索的范围是：

$$
\theta_{t+1}
=
\text{ResearchAgent}
(\theta_t,\;D,\;R_t)
$$

其中 \\(R_t\\) 是累积的实验记录。

这比传统 ML 更接近**自动化科学发现**。

---

## 真正困难的部分：避免虚假改进

这就是金融让问题变得棘手的地方。

如果一个智能体能运行 100 万个实验，最终它会发现：

```text
strategy #837,421
Sharpe = 4.7
```

这很可能是扯淡。

你刚刚制造了一台巨大的**多重检验/过拟合机器**。

因此，一个严肃的自我改进交易系统需要在以下两者之间设置硬边界：

```text
agent-controlled
────────────────────────
hypothesis
code
features
architecture
hyperparameters
experiment selection
```

和：

```text
evaluator-controlled
────────────────────────
data split
future holdout
transaction costs
risk limits
evaluation metric
execution simulator
```

**智能体绝不能能够移动球门柱**。

有趣的是，现在确实有学术研究明确探讨这种架构。2026 年一篇名为 **AQuA** 的论文描述了“递归自我改进的量化交易研究智能体”：这些智能体保留经过验证的实验证据，并用它来指导后续的提议，同时在具有固定数据划分和评估器的密封评估环境中运行。([arXiv][3])

这基本上就是你所问的概念。

### 一个重要的区分

不要将 Griffin 的话理解为：

> “我们构建了持续自我重写并因此印钱的 AGI。”

他实际说的话要务实得多。

他还表示，生成式 AI 对金融的许多领域来说尚未带来革命性变化，因为投资涉及预测变化的未来，而标准 ML 在底层关系相对稳定时尤为强大。他在这方面区分了短期交易和长期投资。([Bishop Rock Capital][4])

所以近期论点是：

> **AI 让研究/工程循环大幅加速 → 人类和机器可以探索更大的假设空间 → 更好的模型/策略得以涌现。**

而不是：

> **LLM 预测明天的股价。**

这就是为什么我认为**“自我改进的交易研究机器”**实际上比“AI 交易员”是更好的描述。

如果你正在考虑自己构建一个，有趣的下一步是将其映射为一个**最小化的自主量化研究循环**——LLM + Python 沙箱 + 回测器 + 实验数据库 + OOS 闸门——然后看看自我改进到底来自哪里。我可以勾勒出这个架构和一个约 200 行的原型。

[1]: https://www.goldmansachs.com/insights/goldman-sachs-exchanges/citadels-ken-griffin-on-ai-us-china-tensions-and-us-data-centers?utm_source=chatgpt.com "Citadel的Ken Griffin谈AI、美中紧张局势与美国数据中心 | Goldman Sachs"
[2]: https://www.bishoprockcap.com/assets/library/ken-griffin/May%202026%20Ken%20Griffin%2C%20Founder%20and%20CEO%20of%20Citadel%20-%20In%20Good%20Company%20%28NBIM%20Investment%20Conference%202026%20stage%29%20%28transcript%29?utm_source=chatgpt.com "Ken Griffin，Citadel创始人兼首席执行官 - In Good Company（NBIM投资大会2026舞台）（文字记录）"
[3]: https://arxiv.org/abs/2608.12841?utm_source=chatgpt.com "AQuA：递归自我改进的量化交易研究智能体"
[4]: https://www.bishoprockcap.com/assets/library/ken-griffin/April%202025%20View%20From%20The%20Top%20with%20Ken%20Griffin%2C%20Founder%20and%20CEO%20of%20Citadel%20%28transcript%29?utm_source=chatgpt.com "与Citadel创始人兼首席执行官Ken Griffin的高峰视角"
