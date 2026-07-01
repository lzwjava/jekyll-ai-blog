---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agent Task Interruption Factors
translated: false
type: note
---

**Question:** Is the claim "if network is stable and the task is routine, long agent tasks generally won't be interrupted" correct?

**Answer:**

**Partially right, but oversimplified.** Network stability is necessary but not sufficient. Here's the full picture:

---

## What Actually Causes Agent Task Interruptions

### 1. Network / Infrastructure (what they're claiming)

- API timeouts, connection drops → **yes, network stability helps**
- Rate limiting (RPM/TPM limits) → network is fine, but you still get cut off
- Provider-side outages (Anthropic, OpenAI) → out of your control

### 2. Context Window Exhaustion — **most common silent killer**

Long tasks accumulate tokens fast:

- Tool outputs pile up
- File contents get read repeatedly
- Multi-turn history grows

Eventually hits `max_context` → agent **dies mid-task**, no warning. This has nothing to do with network.

### 3. Tool / Shell Failures

- A bash command hangs indefinitely → agent waits forever or times out
- File permission errors, missing deps → agent may loop or give up
- Subprocess exits with non-zero → depends on error handling

### 4. Model Hallucination / Logic Loops

- Agent convinces itself a subtask is done when it isn't
- Infinite retry loops on a failing tool call
- "Routine" tasks can still hit edge cases the model handles poorly

### 5. Cost / Token Budget Limits

You're tracking hourly token burn yourself — but if a hard budget cap exists in the agent runner, it will kill the task abruptly.

---

## Verdict

| Condition | Interruption risk |
| --- | --- |
| Network unstable | High |
| Network stable + routine task | **Still moderate** |
| Network stable + long context accumulation | High |
| Network stable + rate limits hit | High |
| Network stable + shell tool hangs | High |

The claim conflates "network stable" with "task will complete." In practice, **context window overflow** and **tool failures** interrupt more long agent runs than network issues do — especially once you've solved the network problem.

**The honest version of the claim:** network stability removes one failure mode, but long agent tasks have at least 4-5 independent failure modes. Routine + short tasks won't interrupt. Long + complex tasks will, eventually.
