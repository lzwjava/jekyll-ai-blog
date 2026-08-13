---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DeepSeek Harness: Everything is a Plugin"
translated: false
type: note
---

Question: what's DeepSeek Harness? Intro to `deepseek-ai/deepseek-harness`

Answer:

DeepSeek Harness is an **agent runtime / agent framework** from DeepSeek. The core idea is:

> **Everything is a plugin.**

Instead of building an AI agent as a fixed pipeline:

```
LLM
 |
Prompt
 |
Tools
 |
Memory
 |
Sandbox
 |
UI
```

DeepSeek Harness treats every component as replaceable:

```
                 Agent Runtime

        +----------------------+
        |       Core Loop      |
        +----------------------+

        /        |        \
     Model      Tools    Memory
      |          |          |
   GPT/Qwen   Shell     Vector DB

        \        |        /
          Everything = Plugin
```

The repository is `deepseek-ai/deepseek-harness`. GitHub describes it as **"DeepSeek Harness: Everything is a Plugin"** and it is implemented mainly in TypeScript.

---

## Why do we need a "harness"?

The word comes from software testing / robotics:

* test harness = environment controlling experiments
* robot harness = control system around capability
* LLM harness = runtime controlling agents

An LLM alone:

```
input -> transformer -> output
```

is not an agent.

An agent needs:

```
observe
  |
reason
  |
choose action
  |
call tools
  |
modify environment
  |
observe again
```

The harness provides this loop.

---

## Compared with LangChain / AutoGen / CrewAI

A rough comparison:

| Framework         | Main idea                                        |
| ----------------- | ------------------------------------------------ |
| LangChain         | composable LLM application library               |
| AutoGen           | multi-agent conversation framework               |
| CrewAI            | role-based agent teams                           |
| OpenAI Agents SDK | simple production agent runtime                  |
| DeepSeek Harness  | plugin-based programmable agent operating system |

The interesting part is the **architecture philosophy**.

LangChain:

```
Chain = A -> B -> C
```

DeepSeek Harness:

```
Runtime
 |
 +-- Model plugin
 +-- Tool plugin
 +-- Sandbox plugin
 +-- Storage plugin
 +-- UI plugin
 +-- Scheduler plugin
```

More like Linux kernel modules.

---

## The "everything is plugin" idea

Example:

Model:

```ts
plugins.model = [
    "deepseek",
    "openai",
    "qwen",
    "local-llama"
]
```

Tools:

```ts
plugins.tools = [
    "shell",
    "browser",
    "git",
    "database"
]
```

Memory:

```ts
plugins.memory = [
    "sqlite",
    "redis",
    "vector-db"
]
```

The agent does not know implementation details.

---

## Why this matters

Current AI agent engineering has a problem:

Every company builds:

```
my-agent/
  prompt.py
  tools.py
  memory.py
  workflow.py
```

After 6 months:

* impossible to swap models
* impossible to replay failures
* impossible to debug
* impossible to benchmark

A harness tries to make agents more like operating systems:

```
Application
    |
Agent API
    |
Agent Runtime
    |
Plugins
    |
Infrastructure
```

---

## Important concept: trajectory

Modern agents need observability.

A good harness records:

```
Session:

User:
"Fix this bug"

Agent:
<thought>
Need inspect repo
</thought>

Tool:
git status

Tool:
pytest

Agent:
Modify file

Tool:
git diff

Result:
success
```

Then you can:

* replay
* debug
* compare models
* train future agents

This is very important for coding agents.

---

## Relation to Claude Code / Codex

The trend is:

### 2023

Prompt engineering:

```
system prompt
+
few examples
```

### 2024

Tool calling:

```
LLM
 |
tools
```

### 2025-2026

Agent runtime:

```
LLM
 |
Harness
 |
Tools
 |
Memory
 |
Environment
```

Claude Code, Codex-style coding agents, SWE-agent, OpenHands all move toward this direction.

---

## For someone building agents, the interesting takeaway

The valuable asset is not the prompt.

Prompt:

```
You are a coding agent...
```

is easy to copy.

The hard part:

```
agent runtime
+
tool ecosystem
+
evaluation
+
trajectory data
+
plugin architecture
```

is the moat.

This is similar to operating systems:

Linux did not win because of one shell command.

It won because it created a stable abstraction:

```
hardware -> kernel -> applications
```

Agent harnesses are trying to create:

```
model -> harness -> agent applications
```

---

## My view

DeepSeek Harness is a signal that the industry is moving from:

> "How do we make a smarter model?"

toward:

> "How do we build reliable autonomous systems around models?"

The next generation of AI companies may not train foundation models. They may build the **agent operating layer**.

References:

* [DeepSeek Harness GitHub](https://github.com/deepseek-ai/deepseek-harness?utm_source=chatgpt.com)
* [DeepSeek GitHub organization](https://github.com/deepseek-ai?utm_source=chatgpt.com)
