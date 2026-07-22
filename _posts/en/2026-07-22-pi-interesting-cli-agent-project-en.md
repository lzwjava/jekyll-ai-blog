---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Pi: Interesting CLI Agent Project"
translated: false
type: note
---

Question: You're asking whether Pi is actually good, given your experience using it and comparing it with Copilot, Claude Code, OpenClaw, Hermes, Codex, Amp, etc.

Answer:

Yes. From what I've seen, **Pi is one of the more interesting recent CLI agent projects**. It isn't trying to beat Claude Code on raw model quality—it optimizes the *agent runtime*.

The things that stand out are:

* **Aggressive context minimization.** Instead of repeatedly stuffing the entire conversation into the prompt, it tries to keep only the information needed for the current step. That reduces latency, token usage, and context drift.
* **Fast iteration.** A lighter context means the forward pass is cheaper, so the agent feels much more responsive.
* **Plugin architecture.** Your `/note` plugin is a good example. A CLI agent becomes much more useful when it can be extended with small commands instead of modifying the core.
* **Unix philosophy.** Pi feels closer to "small composable tools" than "one huge IDE."

Your workflow is a good example:

```
Agent
  ↓
/note
  ↓
ww note queue
  ↓
ww note watch
  ↓
blog
```

That's a much better workflow than manually copying agent responses into notes.

---

Your observation about switching tools also matches what many power users are doing today.

Instead of picking **one** AI IDE forever, people increasingly compose a toolbox:

* Copilot → autocomplete
* Claude Code → large refactors and repo reasoning
* Pi → fast terminal agent
* OpenClaw / Hermes → open-source experimentation
* Codex → OpenAI ecosystem
* Amp → another coding workflow

Each has different tradeoffs in:

* latency
* context management
* tool execution
* pricing
* extensibility

The ecosystem is still evolving rapidly, so switching tools isn't necessarily indecision—it often reflects that the frontier is moving quickly.

One thing I particularly liked from what you described was your `/note` plugin. That's the sort of integration that compounds over time. Saving the last agent response with a single command directly into your knowledge pipeline is the kind of automation that ends up being used dozens of times a day.

As for YOLO mode—if you're using it on a machine you control and understand the risks, many experienced CLI-agent users make the same tradeoff for speed. The `/usr/bin` story is also a good reminder that even experienced users occasionally type a destructive command; having reproducible system setup or good backups makes YOLO mode much less painful.

Overall, I think Pi is a genuinely interesting project—not because it has the strongest model, but because it explores a different point in the design space: **optimize the agent runtime and context management rather than just swapping in a larger LLM.**

References:

* Pi: [https://github.com/earendil-works/pi](https://github.com/earendil-works/pi)
* ww: [https://github.com/lzwjava/ww](https://github.com/lzwjava/ww)
