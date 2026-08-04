---
audio: false
generated: true
image: false
lang: en
layout: post
title: Architecting Reliable Long-Horizon Agents
translated: false
type: note
---

Question: How do you architect an agent to reliably handle long-running / long-horizon tasks (many turns, tool calls, hours of work) without falling apart from context limits?

Answer:

Four mechanisms actually matter. Everything else is glue code.

**1. Externalize state — don't trust the context window as your database**

The context is a cache, not storage. Write plan + progress to disk, re-read on resume. This is what makes a task *resumable* after a crash, a compaction, or even a process restart.

```python
# state.py — the only source of truth
import json, os

STATE_FILE = "task_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {"todos": [], "done": [], "notes": [], "cursor": 0}

def save_state(s):
    json.dump(s, open(STATE_FILE, "w"), indent=2)
```

The agent's system prompt should always instruct: "Before doing anything, read `task_state.json`. After every subtask, update it." This is literally how Claude Code's TODO list works — it's not UI sugar, it's the state machine.

**2. Compaction — trigger early, not at the wall**

Anthropic's own guidance: trigger summarization around 5–20k tokens for simple loops, 50–100k for complex ones — not when you're about to blow the context window compaction should be triggered at roughly 5–20k tokens for some workloads and 50–100k tokens for more complex tasks. Waiting until you're at the limit means you summarize under panic with degraded quality.

```python
def maybe_compact(messages, model_call, threshold_tokens=15000):
    if estimate_tokens(messages) < threshold_tokens:
        return messages
    summary_prompt = (
        "Summarize the trajectory so far: decisions made, files touched, "
        "open questions, next steps. Be dense, this replaces full history."
    )
    summary = model_call(messages + [{"role": "user", "content": summary_prompt}])
    return [
        {"role": "system", "content": messages[0]["content"]},
        {"role": "assistant", "content": f"[compacted history]\n{summary}"},
    ]
```

The key failure mode to know about: **context rot** — degraded performance as tokens grow, independent of whether you're near the limit Chroma's empirical research demonstrates performance degrades as input token count increases across Claude Sonnet 4, GPT-4.1, Qwen3-32B, and Gemini 2.5 Flash — even on intentionally controlled tasks. A 1M token window doesn't fix this — it just moves the cliff Million-token windows do not solve the problem; they shift it.

**3. Sub-agent decomposition — isolate context per subtask**

Instead of one rolling context accumulating everything, spawn a subprocess/subagent per subtask that gets a scoped prompt and returns a short result. This is the "task-decomposition" paradigm vs single-agent accumulation single-agent strategies accumulate the full trajectory, while task-decomposition approaches split work across sub-agents that return shorter results.

```bash
# orchestrator.sh — pattern used in Claude Code's Task tool, also good for CLI agents
for subtask in $(jq -r '.todos[]' task_state.json); do
    result=$(zz agent --isolated --prompt "$subtask" --max-turns 20)
    jq --arg r "$result" '.done += [$r]' task_state.json > tmp && mv tmp task_state.json
done
```

Each sub-agent call is a fresh context — no accumulated cruft from unrelated earlier subtasks. Only the distilled result comes back to the orchestrator.

**4. Structured eviction over naive truncation**

Don't drop-oldest-message. Tag context by type (plan / tool-output / reasoning-trace / decision) and evict by priority + dependency, not recency the agent annotates its trajectory as typed, dependency-linked episodes as work proceeds, and a deterministic, LLM-free policy evicts content in priority order within that structure when a token budget is exceeded. Raw tool outputs (huge log dumps, file contents already applied) are the first to go — decisions and open questions are the last.

**Concrete numbers if you're deciding whether it's worth building this**: combining context editing (compaction) with a persistent memory tool gets meaningfully more than compaction alone Anthropic's internal evaluations show context editing alone delivers a 29% performance lift, and combining it with a memory tool reaches 39%. So: state file (memory) + compaction, not either alone.

For your `zz`/`iclaw` stack specifically: this maps to (a) a `task_state.json` the agent reads/writes every turn, (b) a compaction hook that fires on a token-count check before each LLM call, (c) `--isolated` subagent spawns for anything that would pollute the main trajectory (large file reads, exploratory search).

References:

- [Context Engineering: Agent Reliability Playbook 2026](https://www.digitalapplied.com/blog/context-engineering-agent-reliability-playbook-2026)
- [Beyond Compaction: Structured Context Eviction for Long-Horizon Agents](https://arxiv.org/pdf/2606.11213)
- [Slipstream: Trajectory-Grounded Compaction Validation for Long-Horizon Agents](https://arxiv.org/pdf/2605.08580)
- [Self-Compacting Language Model Agents](https://arxiv.org/pdf/2606.23525)
