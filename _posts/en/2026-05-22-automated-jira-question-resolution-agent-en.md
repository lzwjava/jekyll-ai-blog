---
audio: false
generated: true
image: false
lang: en
layout: post
title: Automated JIRA Question Resolution Agent
translated: false
type: note
---

**Question:** Given ~50 JIRA comments with author + content, how do you design an LLM-powered agent to identify unresolved questions/issues — understanding conversational context (e.g., A asks, B says A's issue is resolved) and categorizing by both person and topic?

**Answer:**

This is a classic **multi-turn conversation understanding** problem. The naive approach (classify each comment independently) fails because resolution is *relational* — it spans multiple comments. You need an agent that reads the full thread, extracts a structured graph of questions→resolutions, then reports gaps.

## Architecture

```
Raw JIRA Comments
      ↓
[Thread Structuring]  ← flatten into chronological thread
      ↓
[LLM: Extract Q&A Graph]  ← one shot, full context
      ↓
{questions: [{id, author, text, resolved_by, category}]}
      ↓
[Filter unresolved]
      ↓
[LLM: Group by category + summarize]
      ↓
Report
```

Two LLM calls is enough. Don't over-agent this.

---

## Implementation

Let me build this as a working artifact you can paste your JIRA comments into:The widget above uses the real Claude API — paste your 50 JIRA comments in `[Author]: text` format and hit analyze.

---

## Design Rationale

**Why single LLM call instead of a chain?**

50 comments fits in one context window (~3-5k tokens). Multi-agent overhead isn't worth it here. The key insight: the model reads the *entire thread at once*, so it naturally handles cross-comment resolution like:
- `[Bob]: Alice's question about load testing is still open` — Bob is referencing Alice, not asking himself
- `[Frank]: Dave's concern was addressed in the design doc` — retroactive resolution with citation

**The prompt engineering that matters:**

```python
system = """
1. Extract every distinct question/issue
2. Determine if resolved — BY ANY COMMENTER, including:
   - Original asker saying "thanks, resolved"
   - Third party saying "X's question is now answered"
   - Implicit resolution ("that design doc covers it")
3. Classify into category
4. Return structured JSON
"""
```

The critical instruction is **"by any commenter"** and **"much later in the thread"** — without this the model naively marks unresolved anything the asker didn't self-close.

**If you had 500+ comments (beyond context window):**

Then you'd actually need an agent loop:

```python
# Chunk → per-chunk extraction → merge pass
chunks = chunk_comments(all_comments, max_tokens=8000)
per_chunk_questions = [extract_questions(c) for c in chunks]
final = merge_and_resolve(per_chunk_questions, all_comments)  # second LLM call
```

The merge pass gets all extracted questions + the full thread summary to adjudicate cross-chunk resolutions.

**Structured output format** is essential — using JSON with `resolved: bool`, `resolvedBy`, `resolutionSummary` means you can filter/sort programmatically without a second parsing pass.
