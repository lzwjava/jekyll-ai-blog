---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Usage Report Breakdown
translated: false
type: note
---

**Question:** How should I interpret the Hermes Insights usage report for the last 30 days?

**Answer:**

This is a usage dashboard for **Hermes** — your custom AI agent/CLI tool. Let me break it down layer by layer.

---

## Token Economics

```
Input tokens:   26,632,983
Output tokens:   1,813,984
Total tokens:  337,052,151   ← this is suspiciously large
```

The total (337M) is ~12x the sum of input+output (28.4M). This means **total tokens includes context window tokens** — i.e., every token *in the context* across all turns, not just new tokens generated. If a session has 100k context and runs 50 turns, that's 5M context-tokens even if only 200k were newly generated. This is the "real cost" metric.

**At your 1.5B/year rate**, 337M in ~21 days = **~5.9B annualized** — you've significantly accelerated your usage.

---

## Model Distribution

| Model | Sessions | Tokens | Role |
|---|---|---|---|
| mimo-v2.5-pro | 185 (70%) | 256M (76%) | Primary workhorse |
| deepseek-v4-pro | 31 | 41M | Heavy reasoning tasks |
| deepseek-v4-flash | 24 | 25M | Fast/cheap tasks |
| glm-5.1 | 25 | 13M | Likely Chinese-context or specific tasks |

Mimo is clearly your default. DeepSeek-v4-pro sessions are fewer but token-heavy (avg 1.3M/session) — you're using it for large-context or complex work.

---

## Tool Call Breakdown — What You're Actually Doing

```
terminal      42.4%   ← you're a shell-first engineer, confirmed
read_file     20.3%   ← heavy codebase reading
search_files  14.9%   ← grep/find patterns in repos
patch         12.0%   ← applying code changes
write_file     4.5%   ← generating new files
execute_code   1.3%   ← running code in-agent
```

This is a **classic agentic coding loop**: read → search → patch → terminal verify. The 12% patch rate against 20% read suggests your agent reads ~1.7 files per patch — very efficient, not thrashing.

`web_search` (0.4%) + `browser_navigate` (0.4%) = you're not using the agent for research much, mostly code work.

---

## Session Patterns

```
265 sessions / 18 active days = ~14.7 sessions/day
Avg session: ~5h 10m   ← long-running agentic tasks
Avg msgs/session: 52.7
```

**5h 10m average session** is wild — these aren't quick Q&A exchanges, these are full autonomous work sessions. The longest was **2.4 days** (May 25) — a single session running across multiple days means your agent is doing deep autonomous work without you restarting it.

**Saturday dominates** (129 sessions = 49% of all sessions). You're doing your deepest AI engineering work on weekends. Weekdays are likely constrained by the bank job.

---

## Notable Sessions — The Outliers

```
Longest:    2.4 days     → persistent autonomous agent run
Most msgs:  378 msgs     → deep back-and-forth, complex task
Most tokens: 3.27M       → large codebase or long-context task
Most tools: 184 calls    → heavy automation session
```

The 184-tool-call session (May 24) with 378 messages is a **multi-hour agentic sprint** — likely a major feature or refactor. That's the kind of session where the agent is doing real engineering work.

---

## TL;DR — What This Tells You About Your AI Usage

1. **You're running Hermes as a persistent coding agent**, not a chatbot. 5h avg sessions confirm this.
2. **mimo-v2.5-pro is your default** — worth evaluating if deepseek-v4-pro gives better output per token for complex tasks.
3. **Context token bloat is 12x raw tokens** — if you're paying per token, long sessions with large contexts are expensive. Consider context compression or session chunking.
4. **You're bottlenecked by weekday time** — Saturday alone is half your usage. If you can automate overnight runs, you'd compound faster.
5. **Skills system usage is low** (24 loads, 11 distinct) — there's headroom to encode more domain knowledge into skills for better agent performance.