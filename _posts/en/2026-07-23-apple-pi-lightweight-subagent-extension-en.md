---
audio: false
generated: true
image: false
lang: en
layout: post
title: Apple-pi Lightweight Subagent Extension
translated: false
type: note
---

Question: What is `https://github.com/dodo-reach/apple-pi`?

Answer:

`apple-pi` is an **extension for the Pi coding agent** that adds **lightweight in-process subagents**. Instead of a single LLM doing everything (planning, searching, editing, reasoning), it lets the parent agent delegate parts of the task to specialized agents running concurrently. ([Pi][1])

Conceptually:

```
           Parent Agent
                │
      delegate(task list)
                │
     ┌──────────┼──────────┐
     │          │          │
  scout      scout      worker
 (Haiku)    (Haiku)    (Sonnet)
 read-only  grep/etc   edit/bash
     │          │          │
     └──────────┼──────────┘
                │
        merge results back
```

The design goals are:

* **Smaller context windows** per subagent.
* **Parallel execution** (`Promise.allSettled`).
* **Different models for different jobs**, e.g.

  * Claude Haiku → repository search
  * Claude Sonnet → code editing
  * GPT-5 → planning
* **No subprocesses**—each subagent is just another `Agent` object in the same process, so spawning them is much cheaper than launching multiple CLI instances. ([Pi][1])

Example workflow:

```
User:
    Refactor authentication.

Parent:
    delegate:
        - find auth code
        - inspect tests
        - implement change

Scout #1:
    grep auth files

Scout #2:
    inspect tests

Worker:
    modify code

Parent:
    summarize + produce final response
```

Each agent is defined as a Markdown file with YAML frontmatter, for example:

```yaml
---
name: scout
description: Fast repository reconnaissance
model: anthropic/claude-haiku-4-5
thinking: off
tools:
  - read
  - grep
  - find
  - ls
---
You only search the codebase.
Never edit files.
```

The extension discovers these agent definitions from:

1. `.pi/agents/` (project)
2. `~/.pi/agent/agents/` (user)
3. bundled defaults

allowing projects to define custom specialist agents. ([Pi][1])

### Why this is interesting

This is very similar to the architecture used by modern agent systems:

* Claude Code's task delegation
* Codex's worker agents
* OpenAI's multi-agent orchestration
* Gemini's planning/execution separation

The key idea is:

> One large context is often less efficient than several focused contexts.

Instead of giving one model 100k tokens, give three smaller agents 10k tokens each, let them work independently, then synthesize the outputs.

Since you've been discussing Pi and CLI-native agents recently, this repository is essentially demonstrating that philosophy inside Pi: **cheap, composable, parallel agent execution rather than a monolithic assistant.**

References:

* Pi package page (README and architecture): [https://pi.dev/packages/apple-pi](https://pi.dev/packages/apple-pi) ([Pi][1])
* Pi project overview: [https://github.com/earendil-works/pi](https://github.com/earendil-works/pi) ([GitHub][2])

[1]: https://pi.dev/packages/apple-pi?page=58&utm_source=chatgpt.com "apple-pi · Packages · Pi"
[2]: https://github.com/earendil-works/pi/blob/main/README.md?utm_source=chatgpt.com "pi/README.md at main · earendil-works/pi · GitHub"