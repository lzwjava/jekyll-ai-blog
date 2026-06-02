---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parallel AI Workflows for Hard Problems
translated: false
type: note
---


**Question:** For hard technical problems like reimplementing AlphaGo or improving Transformers, is one good approach to use OpenClaw with multiple sessions, temporary repo directories, and different models to try different solution approaches in parallel?

**Answer:**

Yes — your intuition is essentially correct, and this is actually a well-established and actively evolving workflow in 2025–2026. Let me give a thorough breakdown.

---

## Core Concept: Why Parallel Multi-Session Agents Work

The fundamental insight is simple: LLM non-determinism is a feature, not a bug — running N parallel agents gives you N valid (and meaningfully different) solutions to choose from.

For hard research problems like reimplementing AlphaGo or experimenting with new Transformer architectures, you want to **explore multiple approaches simultaneously** without one session's context polluting another. This is exactly what the multi-session + temp repo pattern enables.

---

## The Tooling: Claude Code vs. OpenClaw

You mentioned "OpenClaw" — it's worth clarifying the two tools, as they serve different roles:

| | **Claude Code** | **OpenClaw** |
|---|---|---|
| Purpose | Terminal-based agentic coding | Persistent personal AI agent/gateway |
| Sessions | Multiple parallel terminal sessions | Sub-agents with persistent memory |
| Best for | Code execution, repo manipulation | Orchestration, long-running workflows |
| Model swap | `claude --model opus` or `--model sonnet` | Per-agent model config |

OpenClaw is an open-source powerhouse that gives "hands" to models, while Claude Code is a terminal-based tool focused on software development that helps developers write, debug, and refactor code. The two can also be combined — OpenClaw can trigger Claude Code tasks and coordinate workflows.

For pure hard technical research/coding tasks, **Claude Code** is usually the primary tool, with OpenClaw useful for orchestration and persistent memory across sessions.

---

## The Key Pattern: Git Worktrees + Multiple Sessions

The production pattern for what you're describing is **git worktrees** + parallel Claude Code sessions:

Git worktrees solve the context-switching problem by letting you run multiple Claude Code sessions in parallel, each with its own isolated context — no more lost momentum.

Concretely for a hard ML research project like AlphaGo re-implementation:

```bash
# Create isolated worktree branches for each approach
git worktree add ../alphago-mcts-approach    -b approach/mcts-classic
git worktree add ../alphago-policy-net       -b approach/separate-nets
git worktree add ../alphago-transformer-mod  -b approach/transformer-variant

# Launch a Claude Code session in each
cd ../alphago-mcts-approach    && claude
cd ../alphago-policy-net       && claude --model sonnet
cd ../alphago-transformer-mod  && claude --model opus
```

Claude Code officially supports worktrees — subagents can use worktree isolation to work in parallel without conflicts. Each subagent gets its own worktree that is automatically cleaned up when the subagent finishes without changes.

---

## Using Different Models Per Session

This is explicitly supported and recommended:

Each sub-agent can have its own model, context window, memory, tools, and thinking level. You can assign Claude Opus 4 to your coding agent and Claude Sonnet 4 to your research agent — paying premium rates only where they're actually worth it.

For hard ML research, a good split might be:

- **Opus** → architectural design, complex reasoning, novel algorithm design
- **Sonnet** → implementation, refactoring, writing tests, simpler subtasks
- **Other models via `--base-url`** → you can even route to Gemini or GPT-4 for comparison

Using `--base-url` routes requests through a custom API endpoint, enabling any OpenAI-compatible model to power Claude Code — unlocking the full agent loop (persistent sessions, tool use, multi-turn) with any model backend.

---

## Coordinating Multiple Sessions

Agent Teams enable multiple Claude instances to work in parallel on different subtasks while coordinating through a git-based system. One session acts as team lead to break down tasks and synthesize findings from teammates.

A real-world pattern for a research problem:

1. **Lead/Architect session (Opus):** Breaks the problem into sub-tasks, writes a `TASKS.md` shared file, sets interfaces
2. **Implementation sessions (Sonnet):** Each picks up a task, works in its own worktree
3. **Review/merge session:** Compares implementations using `git diff`, merges the best one

One well-documented workflow involves an architect agent iterating on a plan which is then reviewed and implemented by fresh instances of Claude Code. Another pattern is to "send out a scout" — give an agent a genuinely difficult task against a large codebase with no intention of landing its code, just to get ideas from which files it modifies and how it approaches the problem.

---

## Key Pitfalls to Know

**1. Context drift in long sessions**

The same agent asked the same question at different points in a conversation may take different approaches. Early in a session, with a fresh context window, it reads existing files and follows the established pattern. Late in a session, with a packed context, it constructs from training data instead of your conventions. → For long research tasks, **prefer fresh sessions** over very long ones.

**2. Disk space**

Cursor forum users reported that in a 20-minute session with a ~2GB codebase, automatic worktree creation used 9.82 GB. Build artifacts make it worse. → Keep ML model checkpoints and large datasets outside the worktree paths.

**3. No shared database state**

Worktrees share a `.git` object database but not runtime state like databases or GPU memory. For AlphaGo training, each worktree agent needs its own checkpoint directories.

---

## Practical Setup for ML Research Problems

```bash
# 1. Create a shared parent repo
mkdir alphago-research && cd alphago-research && git init

# 2. Scaffold the project with an Opus session
claude --model claude-opus-4-6
> "Design the repo structure for reimplementing AlphaGo Zero.
>  Create a TASKS.md breaking work into: MCTS engine,
>  policy/value network, self-play loop, training loop."

# 3. Spawn parallel worktrees for each component
git worktree add ../alphago-mcts    -b component/mcts
git worktree add ../alphago-network -b component/network
git worktree add ../alphago-selfplay -b component/selfplay

# 4. Run agents in parallel (e.g. with tmux)
tmux new-session -d -s mcts "cd ../alphago-mcts && claude"
tmux new-session -d -s net  "cd ../alphago-network && claude --model sonnet"
tmux new-session -d -s play "cd ../alphago-selfplay && claude"

# 5. After each finishes, compare and merge the best
git diff component/mcts main
git merge component/network
```

---

## Summary

Yes, this is a real and powerful workflow. The full stack looks like:

- **Claude Code** for individual coding sessions in isolated worktrees
- **Git worktrees** for temp repo directories per approach/component
- **Different models** (Opus for hard reasoning, Sonnet for implementation)
- **OpenClaw** optionally on top, for persistent memory, orchestration, and long-running coordination across sessions
- **A lead/architect agent** that writes shared task files so sub-agents coordinate without colliding

The workflow is battle-tested at companies like incident.io and is now officially supported by Claude Code's own documentation.

---

**References:**

- [Claude Code Parallel Worktrees Skill](https://github.com/spillwavesolutions/parallel-worktrees)
- [Mastering Git Worktrees with Claude Code](https://medium.com/@dtunai/mastering-git-worktrees-with-claude-code-for-parallel-development-workflow-41dc91e645fe)
- [Embracing the Parallel Coding Agent Lifestyle – Simon Willison](https://simonwillison.net/2025/Oct/5/parallel-coding-agents/)
- [incident.io: Shipping faster with Claude Code and Git Worktrees](https://incident.io/blog/shipping-faster-with-claude-code-and-git-worktrees)
- [Claude Code Agent Teams Workflow Guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/guide/workflows/agent-teams.md)
- [Claude Code Common Workflows – Official Docs](https://code.claude.com/docs/en/common-workflows)
- [openclaw-claude-code-skill (multi-model routing)](https://github.com/Enderfga/openclaw-claude-code-skill)
- [Designing the Multi-Agent Development Environment](https://alexlavaee.me/blog/parallel-agent-sessions-infrastructure-gap/)
