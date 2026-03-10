---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLMs 过度使用 定价过高 炒作过度
translated: true
type: note
---

---

**问题：** 调用 LLM API 的不受欢迎或反传统观点有哪些？例如，LLMs 比常规代码执行慢且昂贵，你应该只在真正必要时使用它们。

**回答：**

这是一个真正重要的工程视角，却没有得到足够的讨论。以下是对调用 LLM API 的不受欢迎（但合理）真相的全面分解：

---

## 1. 如果代码能做到，就用代码——而不是 LLM

这或许是最被低估的原则。随着 LLMs 成为新宠，一些开发者可能会在不合适的地方使用它们。对于发送电子邮件或通知这样的任务，如果你已经有相应的 API，就不需要让 agent 来做。

经验法则：**如果问题是确定性的且基于规则的，就写一个函数。** LLMs 应该保留给真正需要理解自然语言、歧义或创造性推理的任务。

---

## 2. LLMs 本质上是非确定性的——这是一个真正的工程问题

LLMs 本质上是非确定性的，这意味着相同的输入会得到不同的响应。如果你使用 reasoning models 和 AI agents，错误会在后续步骤中累积，前面的错误会被用于后面的步骤。

计算机程序非常擅长确定性——每次都能产生完全相同的结果。与人类不同，LLMs 不会感到无聊、疲倦或不耐烦。但像人类一样——与计算机程序不同——它们每次使用时不会产生完全相同的结果。

这对生产软件来说至关重要。程序代码之所以是确定性的是有原因的。如果你的代码需要控制具有正确性要求的事物，你需要一个可测试的系统，并证明其正确性。

---

## 3. 在 LLM 周围构建可靠性代价高昂

一旦你关心可靠性，你的架构就不再是“调用一个 LLM”，而是变成一个 pipeline。输入被清理和规范化。生成步骤产生候选答案。另一个步骤评估该答案。路由层决定是否使用修改后的 prompt、重试不同的 model，或进行 corrective pass。我们不是将概率转化为确定性——我们通过冗余和验证来减少不确定性。这种减少会消耗计算资源。

简而言之：让基于 LLM 的功能真正可靠，需要远超人们最初预期的工程工作。

---

## 4. LLMs 很昂贵——成本会快速累积

Token 使用是核心成本驱动因素——LLMs 按 tokens（输入 + 输出）收费。长的 prompt、不必要的上下文和冗长的响应会累积成本。每个查询都使用强大的 model，而简单的 model 或纯代码本可胜任，会进一步膨胀成本。高延迟调用还会增加计算使用量。

频繁的 API 调用会显著增加成本，长期成本高于 self-hosting。数据还必须上传到第三方服务器，存在数据泄露和合规风险。

---

## 5. Tool Calling / Agentic Loops 会放大问题

你的 AI agent 为了回答一个只需两个 API 调用的问题，却进行了十二次调用。每个不必要的 tool call 都消耗了 tokens，增加了延迟，并推高了成本。糟糕的 tool-calling 行为通过低效的执行路径和不必要的处理来膨胀成本和延迟。过于详细的 tool schemas 在每次请求中消耗输入 tokens，即使那些 tools 未被调用——如果你的每个 tool 定义有 500 个 tokens，且有十个 tools，那就是用户提问前 5,000 个 tokens 的开销。

---

## 6. LLMs 比常规代码执行慢

即使是优化的 LLM API，也会引入网络往返延迟和推理时间。五个顺序 API 调用，每个 200ms，就是整整一秒的等待时间，即使 LLM 本身瞬间响应。Serverless functions 和 containerized tools 通常有 cold start 惩罚，在实际执行前增加数百毫秒。

对于 string parsing、regex、已知标签的 classification、sorting 或 data transformation 等任务——纯代码的速度快几个数量级。

---

## 7. LLM 输出并不保证正确

LLMs 并不真正“理解”它们产生的内容。它们的货币是词语之间的概率关系。它们并不总能区分事实和虚构——有些输出可能看起来非常可信，但最终却是自信满满的谬误。

LLMs 优化的是 plausibility，而不是 correctness。这意味着 LLM 生成的代码或逻辑可能看起来正确，但行为不正确——有时是灾难性的（一个 benchmark 发现 LLM 写的代码导致 SQLite 速度慢 20,000 倍）。

---

## 8. 数据隐私是一个隐藏风险

这些平台的 API 使用条款细则通常包括它们可以使用你的数据来训练其系统。对于有严格隐私要求（如需要 SOC 2 合规）的客户，向外部系统发送数据是不可行的。

---

## 9. 供应商锁定和可用性风险

没有人能因为需要更新硬件或决定停止支持而关闭你本地托管的 model。对于 cloud APIs，你无法控制 deprecations、定价变更或服务中断。

---

## 何时真正应该使用 LLM API？

当任务真正需要时使用：

- 理解自然语言或歧义
- 开放式文本生成、summarization 或 reasoning
- 没有确定性规则系统能良好泛化的任务
- 偶尔出错可接受且可由人类审查的任务

跳过时：

- regex、SQL query 或 if-statement 能做到
- 需要保证一致、可测试的输出
- 延迟关键（<100ms 要求）
- 处理高容量、成本敏感的 pipeline
- 数据是私密的/敏感的，不能离开你的基础设施

---

## Summary Table

| Concern | Reality |
|---|---|
| Speed | LLMs 比 native code 慢 10–1000 倍 |
| Cost | 按 token 计费；在大规模时扩展差 |
| Correctness | 概率性的，不保证 |
| Determinism | 设计上非确定性 |
| Testability | 难以可靠地 unit test |
| Privacy | 数据发送到第三方服务器 |
| Reliability | 需要广泛的工程 scaffolding |

底线：**LLMs 是强大的但昂贵的锤子。并非每个问题都是钉子。**

---

**参考文献：**

- [How Poor Tool Calling Behavior Increases LLM Cost and Latency](https://dev.to/amartyajha/how-poor-tool-calling-behavior-increases-llm-cost-and-latency-3idf)
- [LLMs Are Not Deterministic — DEV Community](https://dev.to/marcosomma/llms-are-not-deterministic-and-making-them-reliable-is-expensive-in-both-the-bad-way-and-the-good-5bo4)
- [Deterministic Programming with LLMs](https://www.mcherm.com/deterministic-programming-with-llms.html)
- [Local AI vs APIs: A Founder's Real-World Guide](https://thebootstrappedfounder.com/when-to-choose-local-llms-vs-apis-a-founders-real-world-guide/)
- [Reliability for Unreliable LLMs — Stack Overflow Blog](https://stackoverflow.blog/2025/06/30/reliability-for-unreliable-llms/)
- [6 Pitfalls to Avoid with LLMs — The Enterprisers Project](https://enterprisersproject.com/article/2023/5/large-language-models-6-pitfalls-avoid)
- [How to Save 90% on LLM API Costs](https://blog.premai.io/how-to-save-90-on-llm-api-costs-without-losing-performance/)