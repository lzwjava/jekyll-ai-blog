---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM 应用中的行业网络搜索
translated: true
type: note
---

## 行业如何在 LLM 应用中实现 Web 搜索

简短回答：**主流的生产模式是 native tool calling (function calling)** — 不是单独的“预检查”LLM 调用。但实际上，有**4 种不同的方法**在实际使用中，每种都有权衡取舍。

---

### 方法 1: Native Tool Calling（生产环境中最常见）

这是当今 OpenAI、Anthropic (Claude)、Google Gemini 以及大多数企业系统的工作方式。

您在每个请求开始时向模型声明一个 `web_search` 工具 schema。模型然后**内部决定**是否调用它 — 无需额外的 API 调用。

流程是：系统消息、工具定义和用户消息组合成一个上下文发送给模型。LLM 分析上下文并决定是否需要调用工具。如果是，它输出一个结构化响应，指示调用哪个工具以及使用什么参数。例如，当您询问“OpenAI 的最新新闻”时，代理会思考：*我需要当前信息 — 我应该使用 `web_search` 工具*，然后调用 `web_search(query="OpenAI latest news")`，接收结果，并制定最终答案。

重要的是，LLM 本身不执行函数。相反，它识别合适的函数，收集所需参数，并以结构化 JSON 输出提供信息。然后，这个 JSON 在您的程序运行时环境中被反序列化并执行。

```python
# Example: Declare the tool, model decides when to call it
tools = [{
    "name": "web_search",
    "description": "Search the web for current information",
    "parameters": {"query": {"type": "string"}}
}]
response = llm.chat(messages, tools=tools)
# If response.tool_calls is non-empty → execute search → feed result back
```

---

### 方法 2: Semantic Router（快速，预 LLM 网关）

与其在运行时让 LLM 分类查询，不如使用“Semantic Router”预编码每个意图的示例表述，并通过嵌入空间中的最近邻路由。正如创建者所解释，“与其等待缓慢的 LLM 生成来做出工具使用决策，我们利用语义向量空间的魔力… 使用语义含义路由我们的请求。”

这在**延迟和成本**比灵活性更重要时使用 — 嵌入检查只需微秒，而 LLM 调用需要数百毫秒。适用于企业环境，您提前知道查询类别。

---

### 方法 3: 单独的分类器 LLM 调用（较旧模式，但仍在使用）

通过 function calling 或提示标签使用基于 LLM 的路由，LLM 自然解析用户文本。通过 few-shot 提示或 function schema 很容易实现。缺点：它可能缓慢且昂贵，因为每个决策都是一个 LLM 调用。对于许多工具/意图，提示变得复杂，LLM 可能误分类或幻觉错误的函数。

在模型内置 native tool calling 之前，这种模式更常见。有些团队仍然使用**小型、廉价模型**（例如 GPT-4o mini）仅用于分类意图，而仅使用较大模型进行生成。

---

### 方法 4: 基于规则/启发式预过滤（企业/受限环境）

针对您的特定情况（企业，不允许 Tavily/外部 API），这通常是务实的后备方案：

- 检查查询是否包含时间信号：“latest”、“today”、“current”、“2025”等。
- 检查是否为事实性问题模式（关于现实世界实体的 WHO/WHAT/WHEN）
- 如果是 → 调用您的内部 DDG scraper（如同您文档中的脚本）
- 如果否 → 仅从模型知识回答

这正是**您上传的脚本本质上所做的**，扩展为预调用意图检查 Copilot/model API。

---

### 您的脚本如何融入其中

根据您的文档代码 + Copilot API 上下文，添加的最干净的企业安全模式是：

```python
# Step 1: Ask Copilot/LLM if this query needs a web search
def needs_web_search(query: str) -> bool:
    prompt = f"""Does this query require current/real-time web information to answer well?
Query: "{query}"
Reply with ONLY: YES or NO"""
    response = call_copilot_api(prompt)  # your internal API
    return response.strip().upper().startswith("YES")

# Step 2: If yes, run DDG scrape → inject as context → call Copilot again
if needs_web_search(user_input):
    results = search_ddg(user_input)
    context = format_llm_output(fetch_pages(results))
    final_answer = call_copilot_api(f"Using this web context:\n{context}\n\nAnswer: {user_input}")
else:
    final_answer = call_copilot_api(user_input)
```

---

### 总结：何时使用哪种方法？

| 方法 | 延迟 | 成本 | 灵活性 | 使用场景 |
|---|---|---|---|---|
| Native tool calling | 中等 | 低（1 次调用） | 高 | 标准生产环境 |
| Semantic router | 非常快 | 非常低 | 中等 | 高流量，已知意图 |
| 单独分类器 LLM | 慢 | 高（2 次调用） | 高 | 遗留或复杂路由 |
| 基于规则的启发式 | 最快 | 最低 | 低 | 企业，受限环境 |
| **您的脚本 + Copilot 检查** | 中等 | 低 | 中等 | **企业，无外部 API** |

大多数现代 LLM 内置 tool calling — OpenAI 称之为“function calling”，Anthropic 称之为“tool use”。LLM 意识到需要信息，调用您的 search API，获取结果，并用它们回答。像 LangChain 这样的框架使这变得容易，或者您可以通过 MCP server 连接。但在受限企业环境中，您自己控制搜索层（如您的脚本所做），**意图分类后搜索**模式是实用、经过验证的替代方案。

参考资料：

- [How Tools Are Called in AI Agents (2025)](https://medium.com/@sayalisureshkumbhar/how-tools-are-called-in-ai-agents-complete-2025-guide-with-examples-42dcdfe6ba38)
- [Function Calling in AI Agents — Prompt Engineering Guide](https://www.promptingguide.ai/agents/function-calling)
- [Intent Recognition and Auto-Routing in Multi-Agent Systems](https://gist.github.com/mkbctrl/a35764e99fe0c8e8c00b2358f55cd7fa)
- [Function Calling Using LLMs — Martin Fowler](https://martinfowler.com/articles/function-call-LLM.html)
- [8 Web Search APIs for AI Agents](https://medium.com/@fardeenxyz/8-web-search-apis-you-need-to-know-about-if-youre-building-ai-agents-3028aab6e43d)
