---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude's Dual Knowledge Sources Explained
translated: false
type: note
---

**Question:** How does Claude analyze things — does it use web search, or just model knowledge (with a cutoff date)? And is this a good question to ask a Hermes-style agent?

**Answer:**

## How Claude Analyzes

Two modes, depending on the question:

### 1. Model Knowledge (default)
- Baked-in during training, cutoff **~August 2025**
- Used for: CS fundamentals, math, architecture patterns, code, anything stable
- Fast, no latency, no hallucinated URLs
- Risk: stale on anything post-cutoff (new model releases, API changes, recent papers)

### 2. Web Search (when triggered)
- Live fetch via search tool
- Triggered automatically when: recency matters, you ask about current events, prices, who holds a role, recent releases, etc.
- Also triggered manually if I judge the topic is fast-moving (e.g. "latest Claude API pricing")
- You can also explicitly say **"search for X"** to force it

The heuristic I use:
```
if topic.is_stable() → model knowledge
if topic.requires_current_state() → web_search first, then answer
if topic.is_ambiguous() → search to verify
```

---

## Is This a Good Question for a Hermes-Style Agent?

Yes — and here's exactly why it's a **well-structured agent query**:

```
"Do you use tool X or capability Y for task Z?"
```

This is **meta-reasoning about the agent's own tool use** — which is exactly the kind of introspective query that:

1. **Tests the agent's self-model** — does it know its own architecture?
2. **Helps you calibrate trust** — knowing *when* to trust model knowledge vs. live search is critical for building reliable pipelines
3. **Surfaces tool-use transparency** — good agents should be explicit about what source they used

For your `hermes-agent` or any agent you're building, this pattern is useful:

```python
# Make your agent declare its source
system_prompt = """
When answering, always end with:
Source: [model_knowledge | web_search | tool:X]
Cutoff risk: [low | medium | high]
"""
```

This gives you **traceable outputs** — critical for AI systems in a bank context where auditability matters.

---

**TL;DR:** I use model knowledge by default, web search when recency matters. Your meta-question about tool use is a sharp way to probe any agent — add source declaration to your own agents for production reliability.
