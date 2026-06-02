---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Claude Code Superpowers Plugins Fail
translated: false
type: note
---

Question: Why does Claude Code's Superpower plugin sometimes get stuck or stop mid-task, with the LLM call dying partway through the process?

Answer:Question: Why does the Superpowers plugin in Claude Code sometimes stop mid-task with the LLM call dying?

Answer:

This is a well-known pain point. There are several compounding reasons why it happens.

---

## The Core Problem: Multi-Step Pipelines Are Fragile

The Superpowers workflow is a **long chain of LLM calls**:

```
Explore context → Ask questions → Propose approaches
    → Present design → Write design doc → Spec review
        → User reviews → Transition to implementation
```

Each arrow is a **separate LLM call**. Any one of them can die — and the whole chain stops.

---

## Reason 1: API Timeout

Claude Code has a known 2-minute timeout limitation on LLM calls. Complex Superpowers steps like "Propose 2-3 approaches" involve:

- Reading the entire project context
- Reasoning about multiple design options
- Generating a structured multi-part response

This can easily **exceed 2 minutes**, causing a silent death.

---

## Reason 2: Stalled SSE Stream (No Chunks Arriving)

A connection can stay open but stop delivering SSE chunks mid-stream — the LLM stream itself has no idle timeout or chunk-activity watchdog. Individual tools have their own timeouts, but the LLM stream does not. A stream-idle timeout should reset on each received chunk, while a total request timeout is a separate hard ceiling.

This is why you see the spinner animating but nothing happening — the connection is technically "alive" but frozen.

---

## Reason 3: Context Window Overload

Superpowers reads a lot of files upfront. If your project is large:

- The context window fills up
- The model slows dramatically before dying
- Or the API silently truncates and fails

---

## Reason 4: MCP / Hook Timeouts Interrupting the Session

MCP server or hook timeouts might be sending an interrupt signal, causing the API response connection to drop and be interpreted as an interrupt. This can happen especially when 7+ MCP servers are configured.

---

## Reason 5: Superpowers Itself Is a Heavy Plugin

After installing the Superpowers plugin, Claude Code can sometimes become completely unresponsive — the session-start hook fires and can freeze the session. Even when it doesn't fully freeze, the session-start overhead adds fragility.

---

## What To Do When It Dies

### Option 1: Resume from Checkboxes
When tasks are partially complete when the session dies, unchecked checkboxes in the plan are the only way the next session knows where to resume. Marking them is the state log, not a formality.

Just tell Claude: **"Continue from where you left off — pick up at 'Propose approaches'"**

### Option 2: Break the Task Into Smaller Pieces
Instead of letting Superpowers run the full pipeline in one shot, manually trigger each phase:
```
/brainstorming   ← run this, wait for it to finish
then
/execute-plan    ← only after spec is complete
```

### Option 3: Reduce Context Load
- Keep `CLAUDE.md` under 20K characters
- Disable unused MCP servers before a long Superpowers session

### Option 4: Increase Timeout Settings
```bash
# Set a higher timeout for session hooks
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=30000 claude
```

---

## Summary

The LLM call dies mid-Superpowers because:

| Cause | Likelihood |
|---|---|
| 2-minute API timeout | Very common |
| SSE stream stalls silently | Common |
| Context window overload | Common on large projects |
| MCP hook interference | Possible if many MCPs configured |
| Plugin session-start overhead | Occasional |

The **workaround** is to treat each Superpowers phase as a manual checkpoint — don't expect the full pipeline to run uninterrupted in one go.

References:

- [Claude Code Timeout Issue #5615](https://github.com/anthropics/claude-code/issues/5615)
- [When Claude Goes Silent - API Timeouts](https://medium.com/@lgallard/when-claude-goes-silent-navigating-api-timeouts-and-model-selection-in-claude-code-aed23146b952)
- [Superpowers Plugin Overview](https://claude.com/plugins/superpowers)
- [The Superpowers Plugin Workflow Guide](https://www.builder.io/blog/claude-code-superpowers-plugin)
- [Subagent hang issue - opencode](https://github.com/anomalyco/opencode/issues/13841)
