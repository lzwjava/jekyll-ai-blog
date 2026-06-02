---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么 AI 模型给出过时的建议
translated: true
type: note
---

**问题：** 为什么像 Grok 或 Claude 这样的 AI 聊天机器人无法推荐更新、更受欢迎的联系方式（例如 HSBC HK 的 "Chat with Us" 功能），而默认推荐较旧的方法如打电话，这是这个限制的根本原因是什么？

**回答：**

您已经识别出一个非常真实且广为人知的将通用 LLM 应用于现实世界机构环境的结构性问题。以下是详细分解：

---

## 核心问题：Knowledge Cutoff + Token Frequency Bias

LLM 是在截至某个日期的大量数据上训练的。如果您询问最近发生的事情——训练截止日期之后——模型很可能没有准确答案。这也意味着 AI 可能没有可用的知识来回答关于较新功能的非常具体和技术性问题。

这正是 HSBC HK 的 **"Chat with Us"** 功能的情况。HSBC HK 积极推广这项应用内消息服务，鼓励客户转到 Support 选项卡并点击 "Chat with Us" 以立即获得帮助，不再需要在电话上等待答案。但是，在此功能变得突出之前——或 HSBC HK 开始将其作为首选渠道之前训练的通用 LLM  просто不会知道推荐它。

除了截止日期之外，还有第二个问题：**token frequency/pattern bias**。LLM 根据训练数据中最常见的模式生成响应。由于“call the hotline”几十年来一直是数十亿网页上的主导客户服务建议，模型在统计上倾向于建议打电话——即使存在更新、更好的选项。它不是遵循 HSBC HK 当前的机构偏好；它是在回荡旧文本的统计权重。

---

## 为什么这在银行环境中特别糟糕

LLM 在执行或引用需要与外部系统交互的任务时可能面临困难——例如处理支付、更新数据库或处理复杂工作流。稳健集成的可用性有限，阻碍了 LLM 促进无缝端到端交易的能力，从而降低了其在客户支持场景中的适用性。

在银行环境中，这一点被放大，因为：

- **机构指令不是公开训练数据。** HSBC HK 内部优先使用 "Chat with Us" 而非电话的政策不是从互联网抓取并放入训练语料库的东西。
- **新功能推出速度快于模型重新训练。** 在客户服务动态环境中，公司政策、产品规格和操作程序不断演变。保持 AI 知识库的新鲜度不仅仅是技术任务——这是关键的业务要求。输入给客户服务 AI 的过时或不准确信息可能导致错误响应、客户不满，并对品牌信誉产生负面影响。
- **Hallucination 风险。** LLM 容易产生幻觉——它们能够编造虚假信息，并以惊人自信和断言的方式填补空白。

---

## 正确解决方案：RAG (Retrieval-Augmented Generation)

行业标准修复方法是 **RAG — Retrieval-Augmented Generation**：

RAG 是一种强大的技术，不需要对 LLM 进行额外训练。它通过在查询时选择并提供相关、当前知识来提供更新的信息，并缓解 LLM 的幻觉问题。

当客户查询进来时，RAG 系统首先在内部知识库——文档、数据库、政策、FAQ 中搜索相关信息。然后，将检索到的、事实性信息作为上下文与客户查询一起提供给 LLM，从而 LLM 使用特定上下文生成准确、相关且有依据的响应。本质上，RAG 赋予 LLM 访问公司集体、最新知识的能力。

对于 HSBC HK 具体来说，正确构建的系统将：

1. 拥有始终更新的知识库，明确说明 **"Chat with Us" 是支付和一般查询的首选首联系方式**。
2. 通过 RAG 在推理时将该政策输入给 LLM。
3. 添加 **guardrails**，以便当数字聊天选项可用且优先时，模型无法默认建议电话。

---

## 总结表格

| 问题 | 根本原因 | 解决方案 |
|---|---|---|
| LLM 推荐打电话而不是 "Chat with Us" | Knowledge cutoff — 该功能在训练数据中不存在或不突出 | 使用实时 HSBC 政策文档的 RAG |
| LLM 统计上默认旧模式 | 训练语料库中对 "call the hotline" 的 token frequency bias | 明确的系统提示指令 + guardrails |
| LLM 忽略 HSBC HK 的机构偏好 | 通用 LLM 未在银行内部 SOP 上训练 | 在 HSBC 特定知识库上进行微调或 RAG |
| 答案中未反映新功能 | 静态训练快照 vs. 快速演进的产品功能 | 持续知识库刷新管道 |

---

您的观察是正确的：**通用 LLM 在没有基于实时、机构特定知识的基础上，从结构上不适合为像 HSBC HK 这样的机构提供准确、合规的政策客户服务指导。** 模型按照自己的逻辑并非“错误”——它只是基于陈旧、通用的训练信号进行优化，而不是遵循 HSBC HK 当前和演进的服务偏好。

**参考文献：**

- [HSBC HK 联系我们 – Chat with Us](https://www.hsbc.com.hk/help/contact/)
- [Generative AI 在客户服务中的限制 – Ada](https://www.ada.cx/blog/getting-around-the-limitations-of-generative-ai-for-customer-service/)
- [RAG 和 LLM 在客户服务中的应用 – deepsense.ai](https://deepsense.ai/blog/ai-in-customer-service-how-rag-and-llms-are-transforming-support-at-scale/)
- [LLM 限制和风险 – Master of Code](https://masterofcode.com/blog/generative-ai-limitations-risks-and-future-directions-of-llms)
