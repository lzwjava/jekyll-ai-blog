---
audio: false
date: 2025-09-11
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 理解LLM温度参数基础
translated: true
type: note
---

在LLM API（如OpenAI、Copilot API、Anthropic等）中，**temperature** 是一个控制模型输出*随机性*或*确定性*的参数。

---

### Temperature 的作用

* **低 temperature（接近0）：**
  模型变得确定性，总是选择最可能的下一个token。
  示例：如果要求定义某个概念，每次都会给出最标准/预期的答案。

* **高 temperature（接近1或更高）：**
  模型更自由地采样，探索可能性较低的token。这会增加多样性、创造性和不可预测性。
  示例：对于头脑风暴、故事创作或生成代码变体，较高的temperature可能更合适。

---

### “0.7”的含义

* `temperature = 0.7` 是一个**适中的平衡点**。

  * 它允许一定的随机性和多样性。
  * 模型不会像`0`那样僵化，也不会像`1.2`那样“狂野”。
  * 这就是为什么**0.7常被用作默认值**，包括类Copilot系统——它在保持可靠性的同时提供创造性结果。

---

### 如何使用

在大多数API中，您可以在请求中将其作为参数传递。例如：

**OpenAI API（聊天补全）：**

```json
{
  "model": "gpt-4.1",
  "messages": [
    {"role": "user", "content": "写一个关于龙和机器人的短故事。"}
  ],
  "temperature": 0.7
}
```

**GitHub Copilot API：**
该参数的工作方式类似。Copilot在内部使用temperature来决定是提供更字面化的补全还是更具探索性的建议。大多数IDE集成将其设置为`0.7`左右，但某些上下文（如代码补全）可能使用较低值以保证稳定性。

---

✅ **经验法则：**

* **0–0.3** → 确定性、事实性、可预测。适用于数学、API文档、配置、单元测试。
* **0.4–0.7** → 平衡、自然的写作、标准编码。大多数情况下的良好默认值。
* **0.8–1.2** → 创造性、探索性、冒险性。适用于头脑风暴、故事、诗歌。

---

您是否还想了解 **temperature 如何与 `top_p`（核采样）交互**？因为这两个参数在Copilot/LLM API中通常都可用。
