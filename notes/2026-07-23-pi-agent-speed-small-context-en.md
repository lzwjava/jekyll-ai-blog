---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Pi Agent Speed: Small Context"
translated: false
type: note
---

**Question: Why is pi agent so fast — is it because the context size is small?**

**Answer:**

Yes, **small context size is one of the main reasons**, but the bigger picture is that pi agent is fast because it is optimized around a **minimal agent loop**.

A typical CLI agent loop looks like:

```
user request
    |
    v
LLM reasoning
    |
    v
tool call (bash/edit/search)
    |
    v
observe result
    |
    v
LLM reasoning again
    |
    ...
```

The cost of every LLM step is roughly:

```
latency ≈ prefill(context tokens) + decode(output tokens)
```

The **prefill phase** is where context length hurts.

Example:

```
Context A:
  system prompt       3k tokens
  tools               2k tokens
  history             20k tokens
  repo snippets       50k tokens
  total               75k tokens

Context B:
  system prompt       2k
  tools               1k
  history             5k
  total               8k
```

For every turn:

```
75k tokens → expensive attention computation
8k tokens  → much faster
```

Especially with transformer attention:

```
Attention(Q,K,V)

QK^T

complexity:
O(n²)
```

Modern kernels and KV cache reduce the pain, but **large context still increases memory bandwidth and latency**.

---

Why pi feels especially fast:

### 1. Small, clean system prompt

Many coding agents carry huge instructions:

```
You are an autonomous coding agent...
Rules...
Safety...
Repository guidelines...
Tool descriptions...
Planning framework...
Memory system...
```

The system prompt alone can be tens of thousands of tokens.

Pi is closer to:

```
You are a coding assistant.
Use tools when needed.
```

Less cognitive overhead.

---

### 2. Fewer forced reasoning steps

Some agents do:

```
plan
  |
research
  |
analyze
  |
summarize
  |
execute
```

Pi often does:

```
think
 |
tool
 |
observe
 |
continue
```

The agent loop is shorter.

---

### 3. Tool surface is small

Every tool definition consumes context:

```
bash:
  description...
  parameters...

edit_file:
  description...
  schema...

browser:
  description...
  schema...
```

20 tools = thousands of tokens.

A small tool set means:

```
less prompt
less distraction
faster inference
```

---

### 4. It relies more on the model capability

This is the interesting part.

A lot of modern agents are "framework heavy":

```
agent = model + orchestration + memory + planner + verifier + router
```

Pi is closer to:

```
agent = good model + shell + filesystem
```

Like the Unix philosophy:

```
small tools
small state
compose well
```

---

Your observation matches why experienced engineers often like pi:

For someone who already understands:

* git
* Linux
* debugging
* code structure
* terminal workflows

the agent does not need a lot of scaffolding.

A 12-year engineer can provide the missing "planning layer" mentally.

The agent only needs to do:

```
grep
read
edit
run
fix
repeat
```

So the optimal setup becomes:

```
human:
  architecture + judgment

pi:
  execution bandwidth
```

This is similar to why many researchers like lightweight environments. Karpathy's "Software 3.0" idea is close: the main interface becomes natural language + tools, but the surrounding system should stay simple.

The tradeoff:

| Agent style            | Strength                    | Weakness                   |
| ---------------------- | --------------------------- | -------------------------- |
| Pi                     | Fast, transparent, hackable | Less hand-holding          |
| Claude Code style      | Strong autonomous workflows | More overhead              |
| Heavy agent frameworks | Complex tasks               | Slower, more failure modes |

For an experienced engineer running long tasks, **small context + direct tool loop is often the sweet spot**.
