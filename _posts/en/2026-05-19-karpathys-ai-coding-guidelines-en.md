---
audio: false
generated: true
image: false
lang: en
layout: post
title: Karpathy's AI Coding Guidelines
translated: false
type: note
---

Question: What are Karpathy's guidelines, and what is the "meta skill" concept within them?

Answer:

## Karpathy's Guidelines — Overview

**Karpathy's Guidelines** refers to a viral GitHub repository (`forrestchang/andrej-karpathy-skills`) containing a single `CLAUDE.md` file. It was created by developer Forrest Chang, who distilled Andrej Karpathy's viral observations about LLM coding pitfalls into a single, actionable `CLAUDE.md` file.

Karpathy-inspired guidelines suggest something very practical: don't just prompt the agent, train its behavior using simple rules. This is usually done through a `CLAUDE.md` file that sits alongside your code. Instead of trying to micromanage every prompt, you define how the agent should think and act. And four principles are enough to fix most real-world issues.

---

## The Problems Karpathy Identified

LLM coding assistants are fast, but they tend to over-engineer, refactor things nobody asked for, and hide assumptions. These are not capability problems — the model can write correct, minimal code — it just defaults to doing too much. Left unchecked, you end up reviewing diffs that are three times larger than they need to be.

Specifically, Karpathy called out three repeating failure patterns:

1. **Hidden Assumptions** — Models make wrong assumptions and run with them without checking, hiding confusion and not surfacing tradeoffs.
2. **Over-Engineering** — Models overcomplicate code and bloat abstractions, implementing 1000 lines when 100 would do.
3. **Unintended Side Effects** — Models change or remove code and comments they don't fully understand, even when it's unrelated to the task.

---

## The Four Principles

The guidelines emphasize:
- Surfacing assumptions and tradeoffs upfront rather than making silent decisions or hiding confusion
- Minimum viable code with no speculative features, abstractions, or error handling beyond what was requested
- Surgical, focused edits that touch only what's necessary and match existing code style without improving adjacent code
- Transforming tasks into verifiable goals with explicit success criteria and multi-step plans that enable independent verification loops

More concisely, the four principles are:

| Principle | Core Idea |
|---|---|
| **Think Before Coding** | State assumptions, ask when uncertain, surface tradeoffs before acting |
| **Simplicity First** | Write the minimum code that solves the problem — no speculative features, no extra abstractions |
| **Surgical Changes** | Only touch what's necessary; don't refactor adjacent working code |
| **Goal-Driven Execution** | Define success criteria upfront; let the agent verify its own output against goals |

The "Goal-Driven Execution" principle specifically captures Karpathy's insight: "LLMs are exceptionally good at looping until they meet specific goals... Don't tell it what to do, give it success criteria and watch it go."

---

## What is the "Meta Skill"?

The `karpathy-guidelines` skill is described as a **meta-skill**. It does not perform a specific task. It constrains how the assistant approaches *any* task. This means it complements task-specific skills without conflict.

In other words, unlike a skill that tells Claude "how to write a commit message" or "how to format a report," the karpathy-guidelines skill governs **the reasoning behavior and discipline** the AI applies to everything else it does. It is a layer above all other skills — hence "meta."

The skill is honest about its trade-off: these guidelines bias toward caution over speed. For trivial tasks, you may want the assistant to just act. For anything non-trivial, the added discipline pays for itself in smaller diffs and fewer surprises.

---

## Signs the Guidelines Are Working

The guidelines are working if you see:
- Fewer unnecessary changes in diffs — only requested changes appear
- Fewer rewrites due to overcomplication — code is simple the first time
- Clarifying questions come before implementation — not after mistakes
- Clean, minimal PRs — no drive-by refactoring or "improvements"

---

## Bigger Picture

The `andrej-karpathy-skills` repo exemplifies what Karpathy calls the "idea file" pattern — sharing ideas rather than implementations. The `CLAUDE.md` file isn't a library anyone imports. It's a set of principles anyone can adapt. This is a new kind of open source: not open code, but open ideas.

References:

- [forrestchang/andrej-karpathy-skills — GitHub](https://github.com/forrestchang/andrej-karpathy-skills)
- [Karpathy's CLAUDE.md Skills File: The Complete Guide — Agentpedia](https://agentpedia.codes/blog/karpathy-claude-code-skills-guide)
- [Karpathy Guidelines: Keeping AI Assistants from Overthinking Your Code — Romain Lespinasse](https://www.romainlespinasse.dev/posts/karpathy-guidelines-skill/)
- [Andrej Karpathy's Claude Code Skills — Medium](https://medium.com/data-science-in-your-pocket/andrej-karpathys-claude-code-skills-3db42cc634c8)
