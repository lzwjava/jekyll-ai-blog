---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why LangGraph Needs Separate Nodes
translated: false
type: note
---

**Question:** Why do you need to build these nodes in a LangGraph `StateGraph`?

**Answer:**

Because LangGraph models your agent as an **explicit state machine** — nodes are the computation units, edges are the control flow. Let me break down what each piece actually does and why it exists.

## The Mental Model

```
START → [agent] → should_continue? → [tools] → [agent] → ... → END
```

This is the classic **ReAct loop** (Reason + Act) made explicit as a graph.

## Why Nodes?

A node is just a function: `(state: MessagesState) -> dict`. It receives the full state, does computation, returns a state update.

```python
def agent_node(state: MessagesState):
    # Calls LLM with current messages
    response = llm.invoke(state["messages"])
    return {"messages": [response]}  # appended to state

def tool_node(state: MessagesState):
    # Executes whatever tool_calls the LLM emitted
    last_msg = state["messages"][-1]
    results = execute_tools(last_msg.tool_calls)
    return {"messages": results}  # tool results appended
```

**You need two separate nodes because they do fundamentally different things:**

| Node | Does | Who calls it |
|------|------|-------------|
| `agent` | LLM inference, decides next action | You (via graph) |
| `tools` | Side effects — API calls, DB queries, code exec | Graph (after agent emits tool_calls) |

Merging them into one node breaks the separation of reasoning vs. acting — you lose the ability to inspect, interrupt, or branch between the two.

## Why `set_entry_point`?

Graph needs to know where execution starts. `agent` goes first because the LLM needs to see the user's message before it can decide whether to call tools.

## Why `add_conditional_edges`?

After `agent` runs, you branch:

```python
def should_continue(state: MessagesState):
    last = state["messages"][-1]
    if last.tool_calls:      # LLM wants to call a tool
        return "tools"
    return END               # LLM gave final answer
```

This is the **ReAct decision point** — did the LLM emit `tool_calls` in its response, or a plain text answer? Without this conditional, you'd either always call tools (wrong) or never call them (useless).

## Why `add_edge("tools", "agent")`?

After tools execute, results go back to the LLM as `ToolMessage`s. The agent re-runs with the new context. This is the **loop** — it's what makes multi-step tool use possible.

```
agent → (tool_calls?) → tools → agent → (tool_calls?) → tools → ... → END
```

Without this back-edge, it's a one-shot: call tool once, done.

## What `MessagesState` does

It's just a typed dict with an `messages: Annotated[list, add_messages]` field. The `add_messages` reducer **appends** rather than overwrites, so the full conversation history accumulates:

```
[HumanMessage, AIMessage(tool_calls=[...]), ToolMessage, AIMessage("final answer")]
```

Each node sees the growing history — that's how the LLM has context across turns.

## Why not just write a while loop?

You could:

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

This works but you lose: checkpointing/persistence, streaming per-node, human-in-the-loop interrupts, parallel tool execution, observability hooks, and the ability to swap subgraphs. LangGraph gives you all that by making the loop **explicit and inspectable**.

The graph *is* the while loop — just with superpowers.
