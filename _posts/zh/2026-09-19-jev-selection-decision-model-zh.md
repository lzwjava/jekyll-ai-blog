---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jev：选择决策模型
translated: true
type: note
---

**Jev 模型简介——专为选择/决策设计的模型**

答案：

![Image](https://images.openai.com/static-rsc-4/5kqEB-_tozfNOxCG5znnHmqUzK3eVZlPTZYMFzj-iEZ60reqAn8jgucSyQOY67dUroTlTFtatsaqS8xhGWNxnhwLQ_CnfjdSPSy9Uu0C7C3NOTItAFJE_P_2pB2F421mFgNSfiZjQSz9Abh6tqI1ndMLjpkYCHZvjxdgpbnwyJb2r_FUYXwElq73ZXS95Aob?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AYuVQENzmsodM4geyodKL7q2IsXjw22GtLZG9YRuNZu3LmS6zdrPfRbcuggqGJn3j7PmaSbdHv01mS3sFkATv2ozn1S9anmsFftkrE_5KsIC7uO8BEPiyJrxaT96XM_SPvGecvlbah6SsvWPNiwweM8u09A30YZgPBrI1NJv5TgcANJYnkBh5SnuHiptSQ10?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/PF0HiFKxeBoSoUuOMLYq6lO7IXGlDKUR6Rnt3969j9XAczDGSIWCX_5byQg_jTpx61vKijKUotfDYMGTASOAq5FDXNTwMvMl1yhvfZDSrIlGc-BC9ti6-4qtKg0OUPdlvE5OSgP4e3alS3nnrOJ-RNm2yurcEvb9uyKY9jU95ODE6LJOnyE8J_O9RbQ_Q1gw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hCOxyL2LG8fc_mflbvN7D3zqHPv2EVEnhc4vDXzXT3wE1-FaJgZNxLNLUYtRsMYcoSl1xN0xDEXu2_sx-r4rmY_FifM42YZCc1YZIPl3XRuH471S4E_UnxKw_Le5HJsKYf_fOCXfFxB5B70fgVhBU4JrMFZNvB8SGIxa6sY9WGM2FoQGWZZ-pvp1Y7EDWR2T?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/olx9xVOMIm9iBLyhsyYJfQ8F2JUh03zD-R6Lxy0BJikTRdpzo8vkw2xrj-hdchknFJgWLE1IvZ7R5RIPbBgPelBgA0xK_-UBsYWeyXlmOcJF0G0ETK8f-EqkTvDOcjwb59SgtBJVTShCskABd3Q0x0MalY1v0vR2OnKXDZHw-XzPzROLWk0v4ftKmAvOXmkQ?purpose=fullsize)

**Jev 是 TypeSafe AI 推出的一种新型模型，其任务不是生成文本，而是做出小型、结构化的决策。** 它于 2026 年 9 月发布，被 TypeSafe 称为 **“System One”模型**。([System One Models][1])

核心思想是：

> **LLM:** `prompt → 生成的 tokens`
> **Jev:** `状态 + 问题 → 决策 + 概率`

### 1. 它解决的问题

假设你的智能体有 50 个工具：

```text
用户请求
     │
     ▼
┌───────────────┐
│   LLM         │
│ "使用哪个工具？"│
└───────┬───────┘
        │
        ▼
   工具选择
```

你正在使用一个强大的生成式模型来回答一个本质上属于**分类问题**的任务。

例如：

```text
输入：
"查找昨天所有未读邮件。"

选项：
  gmail_search
  github_search
  shell
  browser
  calendar

输出：
  gmail_search
```

Jev 正是为此类决策而设计的。([Jev 智能体][2])

---

## 2. Jev 的基本抽象

可以将其理解为：

```python
decision = jev(
    state=state,
    question=question,
)
```

其中：

```python
state = """
用户想要查找昨天所有未读邮件。
"""

question = Choice(
    "哪个工具应处理此请求？",
    criteria={
        "gmail": "搜索并检索邮件",
        "github": "搜索 GitHub 仓库",
        "shell": "执行本地 shell 命令",
        "browser": "浏览任意网站",
    }
)
```

概念上：

```text
                  state
                    │
                    ▼
             ┌───────────┐
             │    Jev    │
             └─────┬─────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
    gmail       github       shell
     0.93        0.02        0.01
```

应用程序获得的是**类型化的决策**，而不是需要解析的字符串。([System One Models][3])

---

# 3. 三个重要的原语

Jev 目前提供了三类主要的问题。

### Choice（选择）

**“哪一个？”**

```text
哪个模型应处理此请求？

A. small
B. medium
C. frontier
```

输出本质上为：

```json
{
  "choice": "medium",
  "probabilities": {
    "small": 0.12,
    "medium": 0.81,
    "frontier": 0.07
  }
}
```

这是**模型选择/路由**最明显的用途。([System One Models][3])

### Score（评分）

**“这在有序尺度上处于什么位置？”**

例如：

```text
此编码任务难度如何？

1 = 微不足道
2 = 简单
3 = 中等
4 = 困难
5 = 极其困难
```

然后你的应用程序可以进行路由：

```python
if score < 2.5:
    use_small_model()
else:
    use_frontier_model()
```

### Noul（布尔判断）

**“这个陈述为真吗？”**

例如：

```text
此请求是否需要人工审核？
```

输出：

```text
P(yes) = 0.87
```

这对于门控很有用：

```python
if p_human_review > 0.8:
    escalate()
```

重要的区别在于：**应用程序拥有阈值控制权**；Jev 提供概率，而不是替你决定业务策略。([AutoJev][4])

---

# 4. 为什么这对智能体有意思

这可能是你最感兴趣的部分。

现代智能体包含大量微型决策：

```text
                 智能体状态
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       使用哪个工具？  风险多大？  使用哪个模型？
          │           │           │
          ▼           ▼           ▼
         Jev         Jev         Jev
          │           │           │
          ▼           ▼           ▼
        工具 A       0.12        Haiku
```

然后，昂贵的生成式模型专注于真正的生成工作：

```text
                  ┌──────────────┐
                  │     Jev      │
                  │   决策       │
                  └──────┬───────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           路由       安全       分级
              │          │          │
              └──────────┼──────────┘
                         ▼
                  ┌──────────────┐
                  │ 前沿 LLM     │
                  │ 生成         │
                  └──────────────┘
```

这就是架构理念：**不要在智能体内部为每个决策都使用生成式 LLM。**([Jev 智能体][2])

---

# 5. Jev 用于模型选择

这正是“用于选择的模型”这一名称变得有趣的地方。

假设你有：

```python
models = {
    "cheap": "small-fast-model",
    "normal": "medium-model",
    "hard": "frontier-model",
}
```

与其使用：

```python
router_llm("我应该使用哪个模型？")
```

不如这样构建：

```text
STATE:
    用户请求

QUESTION:
    哪个批准的模型应回答这个问题？

OPTIONS:
    cheap
    normal
    hard
```

然后：

```text
                    用户请求
                         │
                         ▼
                       Jev
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           cheap       normal       hard
           0.61         0.31        0.08
             │
             ▼
       cheap 模型
```

这就创建了一个**模型级联**：

```text
             请求
                │
                ▼
              Jev
                │
       ┌────────┴────────┐
       │                 │
    easy/cheap          hard
       │                 │
       ▼                 ▼
   廉价 LLM          前沿 LLM
```

路由器本身需要极其廉价，否则会破坏路由的经济性。这是 Jev 提出的用例之一。([Jev 智能体][5])

---

# 6. Jev 与普通 LLM 的对比

概念上的差异相当深刻。

普通自回归 LLM 的工作方式：

```text
x
↓
隐藏状态
↓
下一个 token 分布
↓
token
↓
下一个 token 分布
↓
token
↓
...
↓
"使用模型 B 因为……"
```

Jev 则旨在实现更接近：

```text
状态
  ↓
表示
  ↓
决策分布
  ↓
Choice / Score / Noul
```

因此，如果你的应用程序需要：

```text
"编写一个 Python 程序"
```

请使用 LLM。

如果需要：

```text
"我应该调用哪个 Python 工具？"
"

Jev 就是为这类工作而提出的模型类型。

这就是为什么 TypeSafe 将其描述为 **System One**，而不是另一个通用聊天模型。([WorkerKit][6])

---

# 7. 真正重要的区别

不要认为：

> **Jev = 更好的 LLM**

而应认为：

> **Jev = 位于 LLM/智能体之下的专门化学习决策函数。**

你的技术栈可能变成：

```text
                    ┌────────────────────┐
                    │    应用程序        │
                    └─────────┬──────────┘
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
             ┌─────────┐            ┌───────────┐
             │   Jev   │            │    LLM    │
             │  决策   │            │   生成    │
             └────┬────┘            └─────┬─────┘
                  │                       │
          ┌───────┼────────┐              │
          ▼       ▼        ▼              ▼
        路由   门控   评分         文本/代码/工具参数
```

这种分离是有趣的想法。

还有一个重要的限制：**有界输出并不意味着判断一定正确。** 分类器只能从你允许的选项中选择，但仍可能选错。关于 Jev 的独立讨论也指出，某些已公布的准确率数据是基于与其他 LLM 的一致性，而非客观真实情况。([Progressive Robot][7])

对于构建**智能体框架**的人来说，我建议特别关注 Jev 作为可能的**路由器/验证器/工具选择器**，而不是将其视为 GPT/Claude 风格生成的替代品。

参考文献：

* [TypeSafe AI — Jev 概述](https://typesafe.ai/?utm_source=chatgpt.com)
* [Jev 模型解释](https://systemonemodels.org/models/jev/?utm_source=chatgpt.com)
* [Jev 用于 LLM 模型路由](https://jev-agent.com/use-cases/llm-model-routing?utm_source=chatgpt.com)
* [Jev 用于智能体工具选择](https://jev-agent.com/use-cases/agent-tool-selection?utm_source=chatgpt.com)

接下来我可以向你展示**Jev 如何在 `ww`/`iclaw` 风格的智能体中替代模型选择/路由器层**，并附上一个极简的 Python 实现。

[1]: https://systemonemodels.org/guides/jev-explained/?utm_source=chatgpt.com "Jev explained: TypeSafe AI's decision model | System One Models"
[2]: https://jev-agent.com/use-cases/agent-tool-selection?utm_source=chatgpt.com "Jev for agent tool selection — pick from 100 tools | Jev Agent"
[3]: https://systemonemodels.org/models/jev/?utm_source=chatgpt.com "Jev AI model: specs, pricing and use cases | System One Models"
[4]: https://autojev.ai/jev-model?utm_source=chatgpt.com "Jev Model Guide: Inputs, Outputs and Best Use Cases"
[5]: https://jev-agent.com/use-cases/llm-model-routing?utm_source=chatgpt.com "Jev for LLM routing — pick the cheap model first | Jev Agent"
[7]: https://www.progressiverobot.com/2026/09/16/jev-model-typesafe-programmatic-logic/?utm_source=chatgpt.com "Jev Model: Proven Speed, Smart Logic Without a Chatbot"
