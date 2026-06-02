---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Contexts and Code Length Limits
translated: false
type: note
---

**Question:** Given that LLMs now handle 400k–1M token contexts, do we still need to keep scripts at 200–300 lines? Is 800–1k lines fine for a single self-contained Python script, and when should you decouple?

**Answer:**

Yes, 800–1k lines for a self-contained CLI tool is totally fine. The old "200 line limit" was a heuristic for *human* readability and maintenance — it predates LLM-assisted development where your entire codebase fits in context.

## The new mental model

The real constraint isn't line count, it's **cognitive units**:

```
Old world: human holds ~200 lines in working memory
New world: LLM holds ~800k tokens = your entire repo
```

So the question shifts from "how short?" to "what's the right unit of encapsulation?"

## When 800–1k lines in one file is correct

For a CLI agent like `ww`, a single file is *better* when:

- **It's a tool, not a library** — no one imports it, they run it
- **Self-contained execution** — dependencies are explicit at the top, behavior is clear end-to-end
- **LLM-assisted maintenance** — you paste the whole file into Claude/GPT for edits; no cross-file context chasing
- **Fast iteration** — one file to edit, one file to ship, no import graph to untangle

Your `ww` repo is exactly this pattern. A 900-line `ww.py` that does LLM orchestration, tool dispatch, and CLI parsing in one place is *easier* to work with than splitting into `cli.py`, `tools.py`, `agent.py`, `utils.py` — because decoupling creates invisible coupling through imports, shared state, and interface contracts you have to mentally track.

## When to decouple (the real triggers)

Split only when you hit these concrete thresholds:

| Trigger | Action |
|---|---|
| **Shared logic across 2+ scripts** | Extract to a `lib/` module |
| **Different deploy units** | Separate files (e.g. `server.py` vs `client.py`) |
| **Different test cycles** | Split testable core from CLI glue |
| **File exceeds ~1500 lines** | Probably has two distinct responsibilities — find the seam |
| **Two people editing simultaneously** | Git conflict pressure = natural split signal |

## Practical rule for your `ww`-style tools

```
1 tool = 1 file, up to ~1200 lines
shared utilities across tools = lib/common.py
```

```
ww/
  ww.py          # 900 lines, self-contained agent
  zz.py          # 700 lines, self-contained
  iclaw.py       # 800 lines
  lib/
    anthropic.py # shared API wrapper if 3+ tools use it
    config.py    # shared config/env loading
```

The `lib/` only earns its existence when the duplication across top-level scripts is real and painful — not preemptively.

## The "self-contained is best" principle holds

The strongest argument for keeping a script self-contained is **LLM-in-the-loop editing**. When you paste `ww.py` into Claude to ask "add streaming support" or "add a new tool call", having everything in one file means:

- Full context, no hallucinated imports
- No "also update the handler in `tools.py`" drift
- Diff is localized, review is fast

This is the Karpathy `train_gpt2.py` school — one 1000-line file that a competent person (or LLM) can read top to bottom and fully understand. That's a *feature*, not tech debt.

## Verdict

- **800–1k lines**: green zone for self-contained CLI tools
- **1200–1500 lines**: yellow, check if there are two responsibilities
- **1500+**: find the seam, extract only what's genuinely shared
- **Never** split just to follow the old 200-line convention — that's pre-LLM thinking
