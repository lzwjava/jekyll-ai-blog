---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 你可能不需要LangGraph
translated: true
type: note
---

**问题：** 为什么使用 LangGraph？它是如何工作的？为什么不用纯 Python 加 LLM 客户端呢？

**回答：**

## 简短回答：你很可能不需要它

LangGraph 只适用于一小部分问题。对于你构建的大多数东西——CLI 代理、自动化流水线、提示链——**纯 Python + LLM 客户端更好**。

---

## LangGraph 实际上是什么

LangGraph 将你的代理建模为一个**有向图（DAG 或循环图）**，其中：

- **节点** = Python 函数（LLM 调用、工具调用、逻辑）
- **边** = 节点之间的转换（有条件或固定）
- **状态** = 通过图传递的带类型字典

它构建在 LangChain 之上，增加了：检查点、人在回路中的暂停、流式输出、持久性和循环支持（节点可以循环回来）。

---

## 什么时候 LangGraph 真正值得使用

| 使用场景 | LangGraph | 纯代码 |
|---|---|---|
| 简单的 LLM 调用 | ❌ 过于复杂 | ✅ |
| 线性链（提示→解析→提示） | ❌ 过于复杂 | ✅ |
| 带交接的多代理 | ✅ | 会变得混乱 |
| 带检查点的长时间运行代理 | ✅ | 需要重新发明轮子 |
| 执行过程中人在回路 | ✅ | 很痛苦 |
| 有状态循环（ReAct、反思） | ✅ | 可管理 |
| 简单的 ReAct 代理 | ❌ | ✅ 50 行 |

---

## 纯 Python ReAct 代理（你已经知道的方式）

```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [{
    "name": "run_bash",
    "description": "运行一个 bash 命令",
    "input_schema": {
        "type": "object",
        "properties": {"cmd": {"type": "string"}},
        "required": ["cmd"]
    }
}]

def run_bash(cmd):
    import subprocess
    return subprocess.check_output(cmd, shell=True, text=True)

def agent_loop(user_msg):
    messages = [{"role": "user", "content": user_msg}]

    while True:
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            tools=tools,
            messages=messages
        )

        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "end_turn":
            return next(b.text for b in resp.content if hasattr(b, "text"))

        # 处理工具调用
        tool_results = []
        for block in resp.content:
            if block.type == "tool_use":
                result = run_bash(block.input["cmd"])
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})

print(agent_loop("我的当前目录是什么？这里有哪些文件？"))
```

这就是你的 `ww`/`zz` 代理模式。它有效。可调试。只有 40 行。

---

## LangGraph 中的等价实现

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator

@tool
def run_bash(cmd: str) -> str:
    """运行一个 bash 命令"""
    import subprocess
    return subprocess.check_output(cmd, shell=True, text=True)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

llm = ChatAnthropic(model="claude-sonnet-4-6").bind_tools([run_bash])

def call_model(state):
    return {"messages": [llm.invoke(state["messages"])]}

def should_continue(state):
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode([run_bash]))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")
app = graph.compile()

result = app.invoke({"messages": [("user", "我的目录里有什么？")]})
print(result["messages"][-1].content)
```

更多的样板代码，更多的抽象，更难调试——**结果相同**。

---

## 什么时候图抽象值得

**检查点**（崩溃后恢复、人工审批）：

```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("agent.db")
app = graph.compile(checkpointer=checkpointer)

# 在执行中间暂停以等待人工审批
app = graph.compile(checkpointer=checkpointer, interrupt_before=["dangerous_tool"])
```

**多代理交接**（主管 → 子代理）：

```python
graph.add_conditional_edges("supervisor", route_to_agent, {
    "coder": "coder_agent",
    "researcher": "researcher_agent",
    "finish": END
})
```

在纯 Python 中跨多个代理并共享状态的情况下，这确实很难干净地实现。

---

## 针对你的设置，我的诚实看法

考虑到你的 `ww`/`zz`/`iclaw` 工具和 CLI 优先的工作流：

- **构建单代理工具？** → 纯 Python。一直如此。
- **链接 2-3 个提示？** → 纯 Python。函数组合得很好。
- **构建带有审批步骤或跨会话持久化的东西？** → LangGraph 的检查点值得使用。
- **三个以上专业代理交接工作的多代理系统？** → LangGraph 的图模型体现其价值。
- **将代理作为服务部署以供他人通过 API 调用？** → LangGraph Cloud / LangServe 提供了相关基础设施。

LangChain 生态系统增加了显著的**导入开销、抽象税和调试摩擦**。对于你这种令牌高效、快速迭代的风格，原始 API + Python 几乎总是正确的默认选择。只有在遇到 LangGraph 解决的具体痛点时才考虑它：持久化、人在回路，或复杂的多代理路由。
