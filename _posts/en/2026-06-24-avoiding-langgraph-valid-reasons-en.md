---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Avoiding LangGraph: Valid Reasons?"
translated: false
type: note
---

**Question:** Why have I avoided LangGraph until now, and are my reasons valid?

**Answer:**

Your self-analysis is accurate. Let me validate and sharpen each point:

**1. "My 200-300 lines + LLM calls already work"** — This is the most honest reason, and it's *correct* until it isn't. You've hit the same wall most serious builders hit: hand-rolled agent loops are fine at 1-3 tools, 1 agent, linear flow. They start breaking down at:

- Multi-agent coordination (agent A waits on agent B's output conditionally)
- Cycles with state accumulation (retry loops, reflection patterns)
- Checkpointing / resumability (long-running jobs that crash mid-way)

LangGraph's actual value is the **state graph with persistence** — not the abstractions. If you've never needed checkpoint/resume or true conditional branching between agents, you genuinely didn't need it.

**2. Playground/demo directory disruption** — Real friction. The cognitive cost of "where do I even put this experiment" kills exploration. This is fixable in one hour: create `~/code/langgraph-lab/` today with a barebones `StateGraph` skeleton.

**3. No appropriately-sized project** — This is the real gate. LangGraph makes most sense for:

- Multi-step pipelines where steps can fail independently
- Agent systems with human-in-the-loop checkpoints
- Your `ww`/`iclaw`/`zz` CLI tools if they need branching retry logic

Your bank AI work is actually a perfect candidate — auditable, step-traceable agent workflows fit regulated environments well.

**4. Knew about it since 2023 but waited** — Classic "aware but not activated." Right call honestly — LangGraph in 2023 was rough. The persistence/streaming story matured significantly in 2024-2025.

**The real question now:** What triggered you to use it seriously? That's the signal worth tracking — what project forced the threshold?
