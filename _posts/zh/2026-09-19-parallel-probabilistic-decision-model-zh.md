---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 并行概率决策模型
translated: true
type: note
---

问题：**什么是 TypeSafe AI 的“System One Models”/Jev？**

答案：

这是一个相当有趣的架构理念。关键在于：

> **如果软件只需要一个决策，就不要让 AI 生成文本。**

TypeSafe 将这类模型称为新的 **System One Models** 类别，而 **Jev** 是它们公开的第一个模型。([TypeSafe AI][1])

### 1. 普通 LLM

假设你的应用收到：

```text
客户：
“我同一笔订单被收了两次钱。能退一笔吗？”
```

使用 GPT/Claude 时，你可能会要求：

```text
对这条请求进行分类。

输出 JSON：
{
  "intent": "...",
  "urgency": "...",
  "refund_likelihood": ...
}
```

概念上：

```text
文本
 ↓
LLM
 ↓
token → JSON 字符串
 ↓
解析器
 ↓
验证
 ↓
你的程序
```

LLM 本质上是一个 **next-token 生成器**：

$$
P(x_1,x_2,\ldots,x_n)
=
\prod_i P(x_i|x_{<i})
$$

即使你强制输出 JSON/schema 格式，底层仍然是在生成一系列 token。

---

### 2. Jev 改变了目标

Jev 的做法是：

```text
非结构化状态
        ↓
      Jev
        ↓
类型化概率
```

例如，你可以定义：

```python
questions = {
    "intent": [
        "payment_problem",
        "refund_request",
        "technical_problem",
        "other",
    ],
    "urgency": [
        "low",
        "medium",
        "high",
    ],
}
```

然后 Jev 可能会返回类似这样的概念性结果：

```json
{
  "intent": {
    "payment_problem": 0.91,
    "refund_request": 0.84,
    "technical_problem": 0.03,
    "other": 0.01
  },
  "urgency": {
    "low": 0.02,
    "medium": 0.18,
    "high": 0.87
  }
}
```

你的程序随后决定：

```python
if result["urgency"]["high"] > 0.8:
    escalate_to_human()

if result["intent"]["refund_request"] > 0.8:
    route_to_refund_team()
```

所以 **模型不生成动作**。

模型生成的是**概率信息**，而普通软件决定怎么做。

这就是 TypeSafe 将 Jev 描述为：

> “一种前沿智能的函数调用：非结构化状态输入，类型化概率决策输出。”([TypeSafe AI][1])

---

## 3. 真正重要的部分：并行采样

这可能是最有趣的技术差异。

自回归 LLM 的工作方式：

```text
token 1
  ↓
token 2
  ↓
token 3
  ↓
...
token N
```

每个 token 都依赖于前面的 token。

如果你只需要：

```text
A = 0.8
B = 0.1
C = 0.1
```

生成一个像这样的字符串：

```text
{"A": 0.8, "B": 0.1, "C": 0.1}
```

可以说是浪费资源。

Jev 则声称能够**并行**产生结构化的决策，而不是自回归地生成每个输出 token。TypeSafe 表示这是其在延迟/效率上具有优势的主要原因。([TypeSafe AI][1])

概念上：

```text
             ┌── P(A)
state ───────┼── P(B)
             ├── P(C)
             ├── P(D)
             └── ...
```

而不是：

```text
state
 ↓
token
 ↓
token
 ↓
token
 ↓
token
...
```

这是一个非常不同的优化目标。

---

# 4. 为什么这如此重要？

因为**大多数情况下，软件其实并不需要自然语言文本**。

考虑：

```python
if model.says_something_about_customer:
    ...
```

你不需要：

```text
"根据我的分析，我相信客户可能..."
```

你需要：

```python
customer_is_churning = 0.83
```

或者：

```python
route = "fraud_review"
confidence = 0.97
```

或者：

```python
should_escalate = 0.91
```

这使得 Jev 看起来不像：

```text
ChatGPT
```

而更像：

```text
机器学习推理原语
```

嵌入在普通软件内部。

TypeSafe 明确针对分类、路由、评分、提取、分支、验证、护栏和实时应用等场景。([TypeSafe AI][1])

---

# 5. 置信度实际上是个大事

这可能比速度更重要。

想象一下：

```text
fraud = 0.99
```

对比：

```text
fraud = 0.51
```

你的应用可以：

```python
if fraud > 0.95:
    block()
elif fraud > 0.70:
    human_review()
else:
    allow()
```

所以不再是：

```text
AI → 决策
```

而是：

```text
AI → 概率
          ↓
       软件
          ↓
       决策
```

这是一种更可组合的架构。

TypeSafe 专门使用**面向校准决策的强化学习（RLCD）**来训练 Jev，其目标是校准后的概率，而不仅仅是生成人类偏好的答案。([TypeSafe AI][1])

---

# 6. “零幻觉”需要重要的限定

他们的表述在技术上有趣，但容易被误解。

他们并不是说：

> Jev 永远不会做出错误决策。

而是更接近：

> **Jev 无法产生超出允许类型/schema 的幻觉输出。**

如果你的 schema 是：

```text
{
    route: "sales" | "support" | "fraud"
}
```

模型就不能突然输出：

```text
"route": "banana"
```

或者生成 500 字无关的叙述。

TypeSafe 表示这在数学上由受限的输出空间保证。([TypeSafe AI][1])

但是：

```text
类型安全 ≠ 正确
```

这个区别至关重要。

它仍然可能产生：

```text
route = fraud
confidence = 0.93
```

而正确答案应该是 support。

这是**模型错误**，不是类型错误。

---

# 7. 这个架构其实相当优雅

你可以把未来的智能体想象成这样：

```text
                   ┌──────────────┐
用户/事件 ───────>│    Jev       │
                   │ 智能         │
                   └──────┬───────┘
                          │
                 类型化概率
                          │
                          ▼
                   ┌──────────────┐
                   │ 普通代码     │
                   └──────┬───────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          工具 A       工具 B       人工
```

这与以下架构有很大不同：

```text
用户
 ↓
LLM
 ↓
LLM 决定做什么
 ↓
工具调用
 ↓
LLM 解读结果
 ↓
...
```

第二种架构给 LLM 更多的自由度。

第一种架构让**程序员控制状态机**，而 AI 提供模糊判断。

这就是为什么 TypeSafe 称它们为**“智能 if 语句”**。([TypeSafe AI][1])

---

# 8. 为什么可能便宜/快 100 倍？

他们公布的数据很激进：

* Jev：**每百万输入 token 0.042 美元**
* 报告延迟：**70–500 毫秒**
* 他们的工作流基准测试声称比对比的 LLM 设置**快高达 193.6 倍**
* 并且**便宜 444.6 倍**。([TypeSafe AI][1])

但不要将其理解为：

> “Jev 在一切任务上都比 GPT 便宜 400 倍。”

他们的评估**并非**表明这一点。

他们的优势来自对问题的限制：

```text
LLM：
通用智能
+
文本生成
+
推理
+
结构化输出
+
逐 token 解码

Jev：
决策智能
+
固定输出空间
+
并行输出
+
校准概率
```

他们比较的是**System-One 型工作负载**，而不是任意 ChatGPT 工作负载。

TypeSafe 自己也承认，其工作流基准测试由模型能力团队构建，并且比较存在方法论上的局限性。([TypeSafe AI][1])

---

# 9. 这对智能体非常相关

鉴于你正在构建的内容，这是值得关注的部分。

今天的智能体：

```text
LLM
 ↓
推理
 ↓
选择工具
 ↓
生成参数
 ↓
工具
 ↓
读取结果
 ↓
推理
 ↓
...
```

更复杂的架构可能变为：

```text
              ┌─────────────┐
状态 ───────>│     Jev     │
              └──────┬──────┘
                     │
              概率
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       动作 A     动作 B     人工
```

然后将强大的自回归模型保留给实际需要**生成/推理**的部分：

```text
               ┌── Jev ── 廉价/快速决策
智能体状态 ───┤
               └── LLM ── 昂贵的推理/生成
```

这样一来，对于每个微小的决策，比如：

```text
“我应该重试吗？”
“我应该调用这个工具吗？”
“这个结果可疑吗？”
“这个输出违反政策吗？”
“走哪个路由？”
“置信度足够吗？”
“我应该询问用户吗？”
```

不再需要调用价格 $5–10/百万 token 的前沿模型，而是可以使用专门的决策模型。

这就是 System One 背后更深层的理念。

---

## 10. 我的思维模型

我会这样总结两者的区别：

```text
                     传统 LLM

   世界 ──> token ──> 推理 ──> token ──> 世界
                     昂贵
                     顺序
                     灵活
                     难以约束
```

对比：

```text
                     System One

   世界 ──> 状态 ──> 概率 ──> 程序 ──> 世界
                     并行
                     类型安全
                     校准
                     廉价
```

真正有趣的研究问题是：

> **“智能”中有多大比例实际上需要语言生成？**

TypeSafe 的赌注是：**比我们目前假设的要少得多。**

其创始人 Diogo Almeida 将此描述为刻意偏离 RLHF/聊天方向；TypeSafe 专门围绕机器可消费的决策来构建架构、采样器和 RLCD。([TypeSafe AI][1])

所以，**不要**把 Jev 简单地看作“一个更小的 LLM”。

把它看作：

> **一个学习到的概率决策引擎，恰好在受限类问题上拥有前沿模型级别的能力。**

[TypeSafe 的原始公告](https://typesafe.ai/blog/introducing-system-one-models-and-jev?utm_source=chatgpt.com)
[TypeSafe AI 主页](https://typesafe.ai/?utm_source=chatgpt.com)

接下来我可以进一步分解 **Jev 如何从 LLM/RL 角度实际训练——特别是 RLCD 在数学上可能是什么样子，以及为什么并行采样是可能的**，这可能是最有趣的技术部分。

[1]: https://typesafe.ai/blog/introducing-system-one-models-and-jev "Introducing System One Models & Jev - TypeSafe AI Blog"
