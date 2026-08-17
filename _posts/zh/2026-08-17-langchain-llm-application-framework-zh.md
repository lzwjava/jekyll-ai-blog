---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LangChain：LLM应用框架
translated: true
type: note
---

**问题：什么是 LangChain，作为 AI/LLM 工程师应该如何理解它？**

**答案：**

**LangChain 是一个围绕 LLM 构建软件的应用框架。**

核心理念很简单：

> **LLM 调用 + 工具 + 状态 + 检索 + 控制流 = AI 应用**

无需围绕 `openai.chat.completions()` / Anthropic / 本地模型自行编写所有代码，LangChain 为你提供了连接这些组件的抽象。

### 1. 最简单的 LangChain 程序

概念上：

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-5")

response = llm.invoke("用一段话解释 KV cache")

print(response.content)
```

这基本上就是一个 LLM 封装器。

但当你组合多个操作时，LangChain 会变得更有趣：

```text
用户
 ↓
提示词
 ↓
LLM
 ↓
需要调用工具？
 ├── 是 → 工具 → LLM
 └── 否
 ↓
回答
```

### 2. 重要的抽象层

我会大致从以下层次来理解 LangChain：

```text
                    LangChain
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
      Models          Tools          Retrieval
        │              │              │
   OpenAI/Qwen      Python/API     Vector DB
   Claude/etc.      Browser        Documents
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                    Agents
                       │
                       ↓
                 LangGraph
```

**Models**

针对不同 LLM 的统一接口：

```python
llm.invoke(messages)
```

因此你可以轻松切换：

```text
OpenAI
Anthropic
Google
Qwen
DeepSeek
Ollama
vLLM
...
```

无需重写整个应用程序。

---

**Tools**

工具就是一个模型可以调用的函数。

```python
@tool
def search_database(query: str):
    return db.search(query)
```

LLM 可能会产生类似这样的内容：

```json
{
  "tool": "search_database",
  "arguments": {
    "query": "LangChain"
  }
}
```

你的运行时会执行它，并将结果反馈给模型。

这就是 LangChain 对 **agents** 开始变得有用的地方。

---

**Retrieval / RAG**

LangChain 还提供了以下组件：

```text
PDF
 ↓
文档分割
 ↓
嵌入
 ↓
向量数据库
 ↓
相似度搜索
 ↓
相关片段
 ↓
LLM
```

例如：

```python
docs = loader.load()

chunks = splitter.split_documents(docs)

vectors = embeddings.embed_documents(chunks)

results = vector_db.similarity_search(
    "退款政策是什么？"
)
```

这样你就可以构建 RAG 系统，而无需自行实现每一个连接器。

---

### 3. Chains

LangChain 最初的核心概念就是 **chains**（链）。

例如：

```text
问题
   ↓
检索文档
   ↓
生成提示词
   ↓
LLM
   ↓
回答
```

你可以将其表示为一条管道：

```python
chain = retriever | prompt | llm | parser

answer = chain.invoke(
    {"question": "退款政策是什么？"}
)
```

这种 `|` 组合是 LangChain 的标志性思路之一。

它本质上是函数式组合：

```text
f(x) → y
g(y) → z

g(f(x)) → z
```

---

### 4. Agents

这可能与你正在构建的内容最相关。

一个 agent（代理）大致如下：

```text
                    ┌─────────────┐
                    │     LLM     │
                    └──────┬──────┘
                           │
                    决定下一步动作
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
         search         python        terminal
             │             │             │
             └─────────────┼─────────────┘
                           ↓
                        结果
                           │
                           ↓
                          LLM
                           │
                    继续 / 结束
```

伪代码：

```python
while not finished:
    action = llm.decide(state)

    if action.type == "tool":
        result = execute(action)
        state.append(result)

    elif action.type == "final":
        return action.answer
```

这就是为什么 LangChain 在早期的 agent 热潮中变得流行。

---

### 5. 对于严肃的 agent，LangGraph 更为重要

如今，我会区分：

**LangChain**

> 用于 LLM 应用的组件和抽象。

**LangGraph**

> 用于 agent 的、带状态且可控的执行图。

例如，一个生产级的编码 agent 可能如下所示：

```text
START
  ↓
理解任务
  ↓
检查仓库
  ↓
编写代码
  ↓
运行测试
  ↓
测试通过？── 否 ──→ 调试
  │                    │
 是                    └──→ 运行测试
  ↓
审查
  ↓
DONE
```

这更像是 **状态机 / 工作流引擎**，而不仅仅是“LLM 封装器”。

LangGraph 允许你显式地表示这种状态和控制流。

---

### 6. 为什么不直接自己实现？

当然可以。

以你的工程背景，一个最简 agent 可能只需大约 100 行代码：

```python
messages = []

while True:
    response = llm(messages)

    if response.tool_calls:
        for call in response.tool_calls:
            result = tools[call.name](**call.args)

            messages.append({
                "role": "tool",
                "content": result,
            })
    else:
        break
```

而且说实话，**自己动手实现是理解 agent 的最佳方式**。

LangChain 的价值更多在于其生态：

```text
                   你的 Agent
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Models          Tools           RAG
        │              │              │
   50+ 个提供商    数据库           向量数据库
   流式输出        API              加载器
   结构化输出       搜索             检索器
```

你不需要自己构建每一个集成。

---

### 7. 不足之处

LangChain 也可能变得 **过度抽象**。

你最终可能会得到：

```text
AgentExecutor
  ↓
RunnableSequence
  ↓
RunnablePassthrough
  ↓
RunnableLambda
  ↓
Retriever
  ↓
PromptTemplate
  ↓
ChatModel
```

而实际的操作仅仅是：

```python
result = llm(prompt)
```

这是一个常见的批评点。

对于有经验的工程师，我建议：

> **首先理解底层的 LLM / 工具调用 / 状态机机制，然后在 LangChain 的抽象确实能节省代码量的地方使用它。**

不要把 LangChain 当作根本技术来学习。**LLM、工具调用、检索、状态、调度和推理才是基础。LangChain 是构建在它们之上的基础设施。**

### 8. 我如何在 AI 技术栈中定位它

对于你的工作，我认为生态系统如下：

```text
┌───────────────────────────────────────────┐
│              AI Application               │
│       coding agent / research agent       │
├───────────────────────────────────────────┤
│             LangGraph / Agent             │
│       state + control flow + tools        │
├───────────────────────────────────────────┤
│                LangChain                  │
│       models / tools / retrievers         │
├───────────────────────────────────────────┤
│          OpenAI / Anthropic / Qwen        │
│                  LLM                      │
├───────────────────────────────────────────┤
│       vLLM / SGLang / llama.cpp           │
│              inference                    │
├───────────────────────────────────────────┤
│         CUDA / ROCm / GPU hardware        │
└───────────────────────────────────────────┘
```

考虑到你已经在关注 **mini-sgl、KV cache、调度器、MoE、训练和编码 agent**，我不建议花几周时间“学习 LangChain”。我建议 **花一个下午阅读其核心抽象**，然后自己实现一个简单的工具调用 agent，并与 LangGraph 进行对比。

参考：

* [LangChain 文档](https://docs.langchain.com/?utm_source=chatgpt.com)
* [LangGraph 文档](https://docs.langchain.com/oss/python/langgraph/overview?utm_source=chatgpt.com)
* [LangChain GitHub 仓库](https://github.com/langchain-ai/langchain?utm_source=chatgpt.com)