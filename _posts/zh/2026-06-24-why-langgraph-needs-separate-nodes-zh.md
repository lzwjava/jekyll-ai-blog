---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么LangGraph需要独立节点
translated: true
type: note
---

**问题：** 为什么需要在 LangGraph 的 `StateGraph` 中构建这些节点？

**回答：**

因为 LangGraph 将你的智能体建模为一个**显式的状态机**——节点是计算单元，边是控制流。下面我来分解每个部分的具体作用及其存在的原因。

## 心智模型

```
START → [agent] → should_continue? → [tools] → [agent] → ... → END
```

这是经典的 **ReAct 循环**（推理 + 行动）以图的形式显式呈现。

## 为什么需要节点？

节点只是一个函数：`(state: MessagesState) -> dict`。它接收完整的状态，执行计算，并返回状态更新。

```python
def agent_node(state: MessagesState):
    # 使用当前消息调用 LLM
    response = llm.invoke(state["messages"])
    return {"messages": [response]}  # 追加到状态中

def tool_node(state: MessagesState):
    # 执行 LLM 发出的任何 tool_calls
    last_msg = state["messages"][-1]
    results = execute_tools(last_msg.tool_calls)
    return {"messages": results}  # 工具结果被追加
```

**你需要两个独立的节点，因为它们执行根本不同的操作：**

| 节点 | 功能 | 调用者 |
|------|------|--------|
| `agent` | LLM 推理，决定下一步行动 | 你（通过图） |
| `tools` | 副作用——API 调用、数据库查询、代码执行 | 图（在 agent 发出 tool_calls 后） |

将它们合并到一个节点会破坏推理与行动之间的分离——你将失去在两者之间进行检查、中断或分支的能力。

## 为什么需要 `set_entry_point`？

图需要知道执行从哪里开始。`agent` 先运行，因为 LLM 需要先看到用户的消息，然后才能决定是否调用工具。

## 为什么需要 `add_conditional_edges`？

在 `agent` 运行后，你需要进行分支：

```python
def should_continue(state: MessagesState):
    last = state["messages"][-1]
    if last.tool_calls:      # LLM 想要调用工具
        return "tools"
    return END               # LLM 给出了最终答案
```

这是 **ReAct 决策点**——LLM 在其响应中发出了 `tool_calls`，还是给出了纯文本答案？没有这个条件判断，你要么总是调用工具（错误），要么从不调用（无用）。

## 为什么需要 `add_edge("tools", "agent")`？

工具执行后，结果会作为 `ToolMessage` 返回给 LLM。智能体在新的上下文中重新运行。这就是**循环**——它使得多步骤工具使用成为可能。

```
agent → (tool_calls?) → tools → agent → (tool_calls?) → tools → ... → END
```

没有这条返回边，它只是一次性操作：调用一次工具，结束。

## `MessagesState` 的作用

它只是一个带有 `messages: Annotated[list, add_messages]` 字段的类型化字典。`add_messages` 归约器**追加**而不是覆盖，因此完整的对话历史会累积起来：

```
[HumanMessage, AIMessage(tool_calls=[...]), ToolMessage, AIMessage("final answer")]
```

每个节点都能看到不断增长的历史——这就是 LLM 在多次轮次中拥有上下文的方式。

## 为什么不直接写一个 while 循环？

你可以这样写：

```python
messages = [human_msg]
while True:
    response = llm.invoke(messages)
    messages.append(response)
    if not response.tool_calls:
        break
    for tc in response.tool_calls:
        result = execute_tool(tc)
        messages.append(result)
```

这虽然可行，但你会失去：检查点/持久化、按节点流式传输、人在回路中的中断、并行工具执行、可观测性钩子以及替换子图的能力。LangGraph 通过使循环**显式且可检查**，为你提供了所有这些能力。

这个图本质上就是 while 循环——只是拥有了超能力。