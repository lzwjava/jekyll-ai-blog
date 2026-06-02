---
audio: false
generated: true
image: false
lang: en
layout: post
title: When to Use Skills vs. Simple Prompts
translated: false
type: note
---

**Question:** When should you actually create a "skill" vs. just saving a prompt or using Claude Code directly? Is skill creation only for hard/complex tasks?

**Answer:**

Yes, you've got the right mental model. Here's the clear breakdown:

## When to create a Skill

A skill is justified when **the task is complex enough that a naive LLM call fails**, and you need:

- **Multi-step orchestration** — the task requires a sequence of tool calls, file reads, bash commands, and decisions chained together
- **Environment-specific constraints** — e.g., "use `--break-system-packages`", "write output to `/mnt/user-data/outputs/`", "this library has a quirky API" — things that aren't in the model's training data
- **Repeatability at quality** — you've already trial-and-errored the right approach and want to encode that knowledge so every future run gets it right the first time
- **300+ line implementations** — when the "how to do it correctly" is itself non-trivial code (your `ww` tool is a good example of this threshold)

Skills are basically **compiled institutional knowledge** — the delta between "naive Claude attempt" and "Claude that already did this correctly 10 times."

## When NOT to create a Skill — just save a prompt

For tasks where a well-written prompt in a markdown file is enough:

```
~/prompts/
  summarize-pr.md
  review-python.md
  explain-paper.md
  draft-commit-msg.md
```

Then `cat ~/prompts/summarize-pr.md | pbcopy` or pipe it directly into your CLI agent. This covers:

- **Consistent formatting requests** — "always respond in this structure"
- **Domain-specific context injection** — "assume the codebase is Django + Celery + Postgres"
- **Persona/style constraints** — "be terse, code-first, no preamble"
- **Simple one-shot tasks** — anything Claude gets right on first try with the right context

## The actual heuristic

```
Does naive Claude (no extra context) fail this task?
├── No  → Just prompt. Save it in a .md file if you repeat it.
└── Yes → Does it fail because of missing *knowledge* or missing *orchestration*?
    ├── Missing knowledge (env quirks, library gotchas, your conventions)
    │   → Add a SKILL.md with the encoded know-how
    └── Missing orchestration (multi-step, tool chaining, stateful)
        → Build a script (like ww) OR a SKILL.md that guides the orchestration
```

## Your `ww` tool is already the right instinct

`ww` at 200-300 lines is exactly the right level — it's a **reusable agent harness** where the complexity lives in the Python, not in a skill file. A `SKILL.md` for that would just be:

```markdown
# ww-style CLI agent
Run: python ww.py <task>
The script handles tool dispatch, context injection, and retry logic.
Don't reinvent — extend ww.py directly.
```

The skill file just points to the real implementation.

## TL;DR

| Situation | Solution |
|-----------|----------|
| Repeating a prompt pattern | Save `.md` prompt file |
| Claude fails due to env/library quirks | SKILL.md with constraints |
| Complex multi-step orchestration | Python script (like `ww`) |
| Both quirks + orchestration | SKILL.md + script combo |
| Simple Q&A | Just ask, don't save anything |

Skills are **worth the overhead** only when the encoded knowledge meaningfully improves output quality on a task you'll run repeatedly. For everything else, a prompt file or direct Claude Code invocation is the right call.
