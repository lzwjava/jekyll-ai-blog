---
audio: false
generated: true
image: false
lang: en
layout: post
title: Architectural Limits and Parallel Patterns for AI Agents
translated: false
type: note
---

**Question:** What are the fundamental limits of AI agents (like Hermes or Claude Code) around multi-threading, and what's the right pattern to overcome slowness?

**Answer:**

Yes, you've hit on a real architectural constraint. Let me break it down precisely.

## Why Agents Are Serially Slow

AI agents operate in a **sequential tool-call loop**:

```
think → call tool → wait → observe → think → call tool → wait ...
```

Each step is blocking. The agent can't issue 10 bash commands simultaneously — it issues one, waits for the result, then decides the next. This is inherent to how autoregressive LLMs work: the next token depends on all previous tokens, including tool results.

The LLM itself is the serialization bottleneck. It can *reason* about parallelism, but it can't *execute* it.

## The Two Patterns to Escape This

### Pattern 1: Agent writes parallelized code → you run it

The agent's job shifts from "do the work" to "write the parallel worker". You execute the script.

```python
# Agent generates this; you run it
import concurrent.futures
import subprocess

tasks = [
    "summarize file_a.py",
    "summarize file_b.py",
    "summarize file_c.py",
]

def process(task):
    # each task hits LLM API, does I/O, etc.
    result = subprocess.run(["python", "worker.py", task], capture_output=True)
    return result.stdout.decode()

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(process, tasks))
```

This is the **code-gen escape hatch** — agent reasons about the problem shape once, emits parallelized code, exits the loop.

### Pattern 2: Multi-agent orchestration (parallel sub-agents)

Instead of one agent doing everything serially, an **orchestrator agent** fans out to N **worker agents** running in parallel threads/processes:

```python
import anthropic
import concurrent.futures

client = anthropic.Anthropic()

def run_subagent(task: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": task}]
    )
    return resp.content[0].text

tasks = [
    "Analyze auth.py for security issues",
    "Analyze db.py for N+1 queries",
    "Analyze api.py for missing error handling",
]

with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
    futures = {executor.submit(run_subagent, t): t for t in tasks}
    results = {task: f.result() for f, task in
               [(f, futures[f]) for f in concurrent.futures.as_completed(futures)]}
```

The orchestrator just **plans and dispatches**, workers execute in parallel. This is what Claude Code's sub-agent feature is moving toward.

## The Real Architecture Map

```
                    ┌─────────────────┐
                    │  Orchestrator   │  ← serial LLM loop, but thin
                    │  (plans tasks)  │
                    └────────┬────────┘
                             │ fan-out
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         [Worker 1]     [Worker 2]     [Worker 3]
         (parallel)     (parallel)     (parallel)
              │              │              │
              └──────────────┼──────────────┘
                             │ fan-in
                    ┌────────▼────────┐
                    │  Aggregator     │
                    │  (merge results)│
                    └─────────────────┘
```

The key insight: **LLM serial thinking is cheap (tokens); I/O and compute are expensive**. Push all expensive work into parallel workers, keep the LLM in the orchestrator role only.

## What This Means for Your `ww`/`zz` CLI Agents

Since you're building CLI agents, here's the practical pattern:

```python
# Instead of agent calling tools one by one:
# agent.run("check all 50 repos for outdated deps")

# You structure it as:
def agent_plan(goal: str) -> list[str]:
    """LLM generates the task decomposition"""
    ...

def parallel_execute(tasks: list[str], workers: int = 16) -> list[str]:
    """You execute in parallel, agent never touches this loop"""
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(run_task, tasks))

tasks = agent_plan("check all 50 repos for outdated deps")
results = parallel_execute(tasks)
summary = agent_summarize(results)  # LLM only touches plan + summarize
```

The agent's value is in **planning and synthesis**, not sequential execution.

## The Deeper Limit: Context Window as Serializer

Even with parallel sub-agents, there's another serializer: **the context window**. When you fan-in results, everything has to fit back into one context for synthesis. For 50 parallel results, you either:

- Summarize each before fan-in (hierarchical reduction)
- Use embeddings + retrieval instead of raw concat
- Stream results into a structured store (DB/file), agent queries it

This is why **MapReduce is the right mental model** for AI agents at scale — not threads.

## Bottom Line

You're right — the fix is: **agent writes the parallel code, human/runtime executes it**. The agent should never be in the hot path of parallel I/O. Reserve LLM calls for planning and synthesis; parallelize everything else in code it generates or orchestrates.
