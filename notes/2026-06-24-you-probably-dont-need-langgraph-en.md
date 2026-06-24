---
audio: false
generated: true
image: false
lang: en
layout: post
title: You Probably Don't Need LangGraph
translated: false
type: note
---

**Question:** Why use LangGraph? How does it work? Why not just write plain Python with an LLM client?

**Answer:**

## Short answer: You probably don't need it.

LangGraph is useful for a narrow set of problems. For most things you're building — CLI agents, automation pipelines, prompt chains — **plain Python + LLM client is better**.

---

## What LangGraph actually is

LangGraph models your agent as a **directed graph (DAG or cyclic)** where:
- **Nodes** = Python functions (LLM calls, tool calls, logic)
- **Edges** = transitions between nodes (conditional or fixed)
- **State** = a typed dict passed through the graph

It's built on top of LangChain, adds: checkpointing, human-in-the-loop pauses, streaming, persistence, and cycle support (nodes can loop back).

---

## When LangGraph is actually worth it

| Use case | LangGraph | Plain code |
|---|---|---|
| Simple LLM call | ❌ overkill | ✅ |
| Linear chain (prompt → parse → prompt) | ❌ overkill | ✅ |
| Multi-agent with handoffs | ✅ | gets messy |
| Long-running agent with checkpoints | ✅ | reinvent the wheel |
| Human-in-the-loop mid-execution | ✅ | painful |
| Stateful loops (ReAct, reflexion) | ✅ | manageable |
| Simple ReAct agent | ❌ | ✅ 50 lines |

---

## Plain Python ReAct agent (what you already know)

```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [{
    "name": "run_bash",
    "description": "Run a bash command",
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

        # Handle tool calls
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

print(agent_loop("What's my current directory and what files are here?"))
```

This is **your `ww`/`zz` agent pattern**. It works. It's debuggable. It's 40 lines.

---

## The equivalent in LangGraph

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
    """Run a bash command"""
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

result = app.invoke({"messages": [("user", "What's in my directory?")]})
print(result["messages"][-1].content)
```

More boilerplate, more abstraction, harder to debug — **for the same result**.

---

## When the graph abstraction pays off

**Checkpointing** (resume after crash, human approval):
```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("agent.db")
app = graph.compile(checkpointer=checkpointer)

# Pause mid-execution for human approval
app = graph.compile(checkpointer=checkpointer, interrupt_before=["dangerous_tool"])
```

**Multi-agent handoffs** (supervisor → subagent):
```python
graph.add_conditional_edges("supervisor", route_to_agent, {
    "coder": "coder_agent",
    "researcher": "researcher_agent",
    "finish": END
})
```

This is genuinely hard to wire cleanly in plain Python across multiple agents with shared state.

---

## My honest take for your setup

Given your `ww`/`zz`/`iclaw` tools and CLI-first workflow:

- **Building a single-agent tool?** → Plain Python. Always.
- **Chaining 2-3 prompts?** → Plain Python. Functions compose fine.
- **Building something with human approval steps or persistence across sessions?** → LangGraph checkpointing is worth it.
- **Multi-agent system where 3+ specialized agents hand off work?** → LangGraph's graph model earns its keep.
- **Deploying an agent as a service others hit via API?** → LangGraph Cloud / LangServe has infra for this.

The LangChain ecosystem adds significant **import overhead, abstraction tax, and debugging friction**. For your token-efficient, fast-iteration style, raw API + Python is almost always the right default. Reach for LangGraph only when you're hitting the specific pain points it solves: persistence, human-in-the-loop, or complex multi-agent routing.
