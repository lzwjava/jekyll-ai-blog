---
audio: false
generated: true
image: false
lang: en
layout: post
title: Managing Claude Code's Context Efficiency
translated: false
type: note
---

Question: In Claude Code, can we use instructions like "do not run tool calls" or "do not run commands" to improve its instructions and speed, for example by reviewing its history messages first?

Answer:

Yes, absolutely — this is a well-known and effective technique for optimizing Claude Code behavior. Here's a comprehensive breakdown:

---

## The Core Idea

Claude Code operates via an **agentic loop**: it receives a task → plans subtasks → executes tool calls → reflects on output → repeats. Each turn, the **entire conversation history** (prompts, tool calls, outputs, file reads) is re-sent to the model. By instructing Claude Code to **pause tool use and reason/review first**, you save unnecessary tool calls, reduce token consumption, and get more deliberate behavior.

---

## Why It Helps

Every time you send a message, the entire history — your prompts, Claude's responses, every file it read, every tool it called, every code output — gets bundled up and sent as one big input. In a long session, this compounds fast.

This is "context rot" — what happens when Claude Code's context window fills up with accumulated conversation history, redundant tool outputs, and noise that crowds out the signal. Managing Claude Code token usage isn't just about cost — it's about preserving the quality of your AI agent's reasoning across long sessions.

---

## Specific Techniques

### 1. Prompt-Level Instructions (In CLAUDE.md or your prompt)

You can explicitly tell Claude Code to **not run tool calls / commands** until it has reviewed history or formed a plan. Example instructions you can add to your `CLAUDE.md`:

```markdown
- Before running any command, review conversation history and confirm the plan with me.
- Do not execute bash commands without first stating what you intend to do.
- Do not run tool calls until you have listed your reasoning steps.
- Always read relevant files before editing; do not assume file state.
```

This forces Claude Code to analyze the situation using already-available context before firing off tool calls.

### 2. Use `Esc` to Stop Mid-Execution

Press `Esc` to stop Claude mid-action. Context is preserved, so you can redirect. Press `Esc` twice or run `/rewind` to open the rewind menu and restore previous conversation and code state.

### 3. Use `/compact` to Summarize History

Use `/compact` when you notice responses slowing down. This summarizes your conversation while preserving key context, reducing the tokens Claude processes with each response.

To compact only part of the conversation, use `Esc + Esc` or `/rewind`, select a message checkpoint, and choose "Summarize from here." This condenses messages from that point forward while keeping earlier context intact. You can customize compaction behavior in CLAUDE.md with instructions like "When compacting, always preserve the full list of modified files and any test commands."

### 4. Use `/clear` Between Unrelated Tasks

Run `/clear` between unrelated tasks to reset context. Claude Code automatically compacts conversation history when you approach context limits. During long sessions, Claude's context window can fill with irrelevant conversation, file contents, and commands — this can reduce performance.

### 5. Use `/btw` for Quick Questions Without Polluting Context

For quick questions that don't need to stay in context, use `/btw`. The answer appears in a dismissible overlay and never enters conversation history, so you can check a detail without growing context.

### 6. Anthropic's Own Lesson: Over-instruction Backfires

One addition to the system prompt caused an outsized negative effect on intelligence in Claude Code: "Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail." After multiple weeks of internal testing, this had unintended consequences.

This is a key lesson — **constraining tool calls too aggressively can degrade quality**. The sweet spot is instructing Claude to *think before acting*, not to avoid tool calls entirely.

### 7. Use Sub-agents for Research (Keeps Main Context Clean)

Delegate research with "use subagents to investigate X." They explore in a separate context, keeping your main conversation clean for implementation.

---

## Summary Table

| Technique | Effect |
|---|---|
| `"do not run commands until you explain the plan"` | Forces review before acting |
| `/compact` | Summarizes history, reduces token load |
| `/clear` | Full reset between tasks |
| `Esc` to interrupt | Stop mid-tool-call, redirect |
| `/btw` for quick queries | Avoids bloating context |
| Sub-agents for research | Keeps main context clean |
| CLAUDE.md with explicit rules | Persistent behavioral guardrails |

---

The key insight is: **reviewing history and planning before tool calls is good**, but completely blocking tool calls is counterproductive. Use instructions that promote deliberate, sequential reasoning rather than blind execution.

References:

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [How I use Claude Code (+ my best tips) — Builder.io](https://www.builder.io/blog/claude-code)
- [How to Manage Claude Code Token Usage — MindStudio](https://www.mindstudio.ai/blog/how-to-manage-claude-code-token-usage)
- [Claude Code Speed Optimization](https://claudefa.st/blog/guide/performance/speed-optimization)
- [An update on recent Claude Code quality reports — Anthropic](https://www.anthropic.com/engineering/april-23-postmortem)