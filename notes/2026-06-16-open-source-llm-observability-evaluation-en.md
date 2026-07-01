---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-Source LLM Observability & Evaluation
translated: false
type: note
---

**Question:** What is Langfuse?

**Answer:**

Langfuse is an open-source LLM observability and evaluation platform. Think of it as the "Datadog for LLM apps" — it gives you tracing, evals, prompt management, and dataset tooling in one place.

## Core primitives

```
Trace
 └── Span (generation, retrieval, tool call, etc.)
      ├── input / output
      ├── latency
      ├── token usage + cost
      └── metadata / tags
```

- **Traces** = one end-to-end request through your LLM pipeline
- **Generations** = specific LLM calls within a trace (tracked with model, tokens, cost)
- **Spans** = any other step (retrieval, function calls, agent actions)
- **Scores** = human or automated eval labels attached to traces

## What it actually does

| Feature | What it gives you |
| --- | --- |
| Tracing | Full visibility into multi-step agent/chain calls |
| Prompt management | Version-controlled prompts, A/B test variants |
| Evals | LLM-as-judge, human annotation, custom scoring |
| Datasets | Curate input/output pairs for regression testing |
| Cost tracking | Per-model, per-user, per-feature spend |
| Analytics | Latency p50/p95, error rates, token distribution |

## Quick integration (Python)

```python
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse()  # reads LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY from env

@observe()
def my_pipeline(user_query: str) -> str:
    # auto-traced as a span
    response = call_llm(user_query)

    # attach a score inline
    langfuse_context.score_current_observation(
        name="quality",
        value=0.9,
    )
    return response
```

Or lower-level SDK:

```python
trace = langfuse.trace(name="rag-pipeline", user_id="user-123")
span = trace.span(name="retrieval")
generation = trace.generation(
    name="llm-call",
    model="claude-sonnet-4-6",
    input=[{"role": "user", "content": "..."}],
    output="...",
    usage={"input": 512, "output": 128}
)
```

## Self-hostable

```bash
# docker-compose in ~5 minutes
git clone https://github.com/langfuse/langfuse
cd langfuse
docker compose up
```

Postgres backend, Next.js frontend. You can run it on your Ubuntu workstation at `<IP_ADDRESS>`.

## Why it matters for your stack

Given you're running Claude, DeepSeek, MiMo across CLI agents and banking AI systems — Langfuse lets you:

- Compare latency/cost across models (Claude vs DeepSeek-v4-flash)
- Catch regressions when you update prompts
- Build eval datasets from production traces
- Score agent trajectories automatically (LLM-as-judge)

It integrates natively with LangChain, LlamaIndex, OpenAI SDK, and raw `anthropic` SDK. For your custom CLI agents (`ww`, `iclaw`, `zz`), the decorator pattern is the fastest path to instrumentation.

**References:**

- [Langfuse GitHub](https://github.com/langfuse/langfuse)
- [Langfuse Docs](https://langfuse.com/docs)
- [Self-hosting guide](https://langfuse.com/docs/deployment/self-host)
