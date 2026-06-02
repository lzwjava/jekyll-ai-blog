---
audio: false
generated: true
image: false
lang: en
layout: post
title: Context Management Tradeoffs in Iterative Tasks
translated: false
type: note
---

Question: What are the tradeoffs between `/clear` (new session per task) vs. continuing in one session when doing iterative system tasks like macOS cleanup — and how does context accumulation affect token efficiency, cost, and final output quality?

Answer:

Yes, exactly right. This is fundamentally a **context window management strategy** problem, and it has real cost and quality implications.

## The Core Tradeoff

```
One session (accumulate context)          vs.    /clear between tasks
─────────────────────────────────────────────────────────────────────
+ LLM sees prior findings → better decisions    + Cheaper (fewer tokens)
+ Can reference "what we found before"          + No drift / no stale context
+ Stateful reasoning across steps               + Each turn is fresh/focused
- Token cost grows each turn                    - LLM forgets prior findings
- Old context can confuse later turns           - You re-explain state manually
- Risk of hitting context limit mid-task        - Parallelizable
```

## Three Concrete Strategies

### Strategy 1: Full Session (Stateful)
```
Turn 1: "Run htop, show me top 10 memory hogs"
Turn 2: "Kill Chrome helper processes we found"
Turn 3: "Now check if freed RAM, run again"
Turn 4: "Purge inactive memory, compare before/after"
```
Context accumulates → LLM remembers "Chrome was using 4GB" without you re-stating it. Good for **diagnostic → act → verify** loops.

**Cost**: Each turn pays for ALL prior turns. Turn 4 costs ~4x Turn 1.

---

### Strategy 2: /clear Between Unrelated Tasks
```
[Session A] Diagnose memory → find Chrome is culprit → /clear
[Session B] "Kill all Chrome helpers" (self-contained command)
[Session C] "Set up swap file" (unrelated task)
```
Each session is cheap. No cross-contamination. Works when tasks are **independent**.

---

### Strategy 3: Hybrid — Summarize then /clear
The best pattern for long iterative work:

```
Turn 1-3: Diagnose. Accumulate context naturally.
Turn 4:   "Summarize what we found in 5 bullet points"
          → Copy that summary
/clear
Turn 5:   Paste summary as system context → continue acting
```

You compress the expensive accumulated context into a dense state snapshot, then start fresh. This is essentially **KV cache management by hand** — same reason transformers use sliding windows.

---

## Token Cost Math (concrete)

Assume 500 tokens/turn output, 200 tokens/turn input:

```
Strategy 1 (5 turns, no clear):
Turn 1: 700 tokens
Turn 2: 700 + 700 = 1400
Turn 3: 1400 + 700 = 2100
Turn 4: 2100 + 700 = 2800
Turn 5: 2800 + 700 = 3500
Total input tokens: ~10,500

Strategy 2 (/clear each turn):
5 × 700 = 3,500 total tokens

Strategy 3 (summarize at turn 3, /clear, resume):
Turns 1-3: ~4,200
Summary: ~300 tokens
Turns 4-5: 300 + 700 + 700 = ~2,000
Total: ~6,500
```

**3x cost difference** between worst and best strategy for the same work.

---

## For macOS Cleanup Specifically

The optimal pattern is:

```
Turn 1 (diagnose, keep context):
  → htop / top output
  → vm_stat
  → identify top offenders

Turn 2 (act, still same session — LLM needs Turn 1 findings):
  → kill specific PIDs found in Turn 1
  → purge / sudo memory_pressure

Turn 3 (verify, can /clear if you summarize):
  → "Memory before: X, after: Y. Done."
  /clear
```

The key insight: **keep context alive only as long as the LLM needs to reference prior state to make correct decisions.** Once the diagnostic phase is done and you're in pure execution mode, the prior context is dead weight.

---

## The Mental Model

Think of it like a **CPU register file**:
- Context window = registers (fast, expensive, limited)
- Your clipboard/notes = RAM (cheap, you manage it)
- `/clear` = flush registers

Good programmers don't keep stale values in registers. Good LLM users don't keep stale findings in context. **Evict aggressively, reload only what's needed.**

This is why tools like Claude Code and agentic loops often do automatic summarization — they're implementing this pattern programmatically so you don't have to think about it.
