---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenRouter 令牌使用量暴增解析
translated: true
type: note
---

## 1. **13 trillion tokens** 这一数字是**每天还是每周**？

**13 trillion tokens** 数字指的是**每周 token 使用量**，不是每天。

- 在**2026 年 2 月 9 日结束的那一周**，OpenRouter 处理了大约**一周 13 trillion tokens**。citeturn0news12
- 在**2026 年 1 月初**，约为**每周 6.4 trillion tokens**，这意味着在几周内总量大致**翻倍**。citeturn0news12

其他报告确认了类似规模：

- OpenRouter 上的总每周 token 消耗达到**约 12.1 trillion tokens**，代表**同比 ~12.7× 增长**。citeturn0search3
- 在**2025 年 3 月**，顶级模型的每周使用量仅为**1.24 trillion tokens**；到**2026 年 2 月**，已上升至**每周 ~13.95 trillion tokens**。citeturn0search5

### 近似每日等价值

如果平台每周处理**13T tokens**：

- **每日 ≈ 1.8T tokens/天**

因此正确解释是：

| Metric | Approx value |
|---|---|
| Weekly tokens | ~13 trillion |
| Daily tokens | ~1.8 trillion |

---

# 2. 增长时间线（简化）

增长极其迅速。

| Time | Weekly tokens |
|---|---|
| 2024 | ~0.5T/week |
| Early 2025 | ~1T/week |
| Sept 2025 | ~5T/week |
| Jan 2026 | ~6.4T/week |
| Feb 2026 | ~13T/week |

来源确认了这一轨迹，包括从**2025 年 9 月的 ~5T 每周**跃升至**2026 年初的超过 13T**。citeturn0search1turn0news12

这意味着：

- **从 2024 → 2026 的 ~26× 增长**

---

# 3. token 使用量为什么增长如此迅速

几个结构性原因解释了这一爆发。

## 1. AI agents 取代简单聊天

最大的变化是**agentic workflows**。

不再是：

```
human → prompt → answer
```

现在许多系统运行：

```
AI agent → search → code → call APIs → think → retry → answer
```

这些 workflow 会产生**许多内部模型调用**，从而成倍增加 token 消耗。citeturn0search3

诸如自主编码工具和工作流自动化系统的 agent 平台现在已成为主要驱动力。citeturn0news12

---

## 2. 编码用例主导

编程任务现在消耗 OpenRouter 上**超过一半的所有 tokens**。citeturn0search7

示例：

- AI coding assistants
- autonomous debugging
- code generation pipelines
- automated testing

这些 workflow 需要**长上下文和重复调用**，从而大幅增加 token 量。

---

## 3. 模型价格大幅降低

一些模型比 frontier models **便宜 10–20×**。citeturn0search3

示例定价比较：

| Model type | Price per million tokens |
|---|---|
| Cheap open models | ~$0.30 |
| Frontier models | ~$5–25 |

更低成本 → 开发者运行**更多查询**。

---

## 4. AI 开发者工具爆发

OpenRouter 位于许多工具的背后：

- coding IDE agents
- AI automation tools
- research assistants
- prompt pipelines

它通过一个 API 聚合了**来自 60+ 提供商的 400+ 模型**。citeturn0search3

这使其成为**LLM infrastructure**的枢纽，因此使用量随着整个生态系统增长。

---

# 4. 预计 token 使用量（未来 2 年）

没有官方预测，但我们可以基于历史增长进行估算。

## 观察到的增长

从 2025 → 2026：

```
~1T → ~13T 每周
≈ 13× 年增长
```

增长很可能**放缓但仍保持很高**。

### 保守情景（每年 5×）

| Year | Weekly tokens |
|---|---|
| 2026 | ~13T |
| 2027 | ~60T |
| 2028 | ~300T |

### 中等情景（每年 3×）

| Year | Weekly tokens |
|---|---|
| 2026 | ~13T |
| 2027 | ~40T |
| 2028 | ~120T |

### 激进情景（agent 爆发）

如果 AI agents 大规模扩展：

- **到 2028 年 >500T tokens/周**

---

# 5. 重要视角

OpenRouter 只是**一个 API gateway**，不是整个 AI 生态系统。

大量量也来自：

- direct OpenAI API
- Anthropic API
- internal company inference
- IDE copilots
- enterprise agents

因此全球总 LLM tokens **远大于** OpenRouter 的统计数据。

---

✅ **关键要点**

- **13 trillion tokens 数字是每周**，不是每天。
- 每日等价约为**~1.8 trillion tokens/天**。
- 增长主要由**AI agents、编码自动化和更便宜的模型**驱动。
- 如果趋势持续，**平台总计每周 100T+ tokens 可能在 2 年内发生**。

---

如果您想看，我也可以展示**全球总 LLM tokens 估算（OpenAI + Anthropic + Google + 中国模型）**——真实数字可能**是 OpenRouter 的 10–20×**，这相当惊人。

References:

- <https://www.businessinsider.com/openclaw-ai-demand-token-use-surge-nvidia-pricing-jumps-2026-2>
- <https://dataconomy.com/2026/02/25/chinese-ai-models-hit-61-market-share-on-openrouter>
- <https://eu.36kr.com/en/p/3700980530851712>
- <https://gigazine.net/gsc_news/en/20251208-empirical-100-trillion-token-study>
