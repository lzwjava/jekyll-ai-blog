---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Custom Instructions Setup Guide
translated: false
type: note
---

Question: How do I set custom instructions for Hermes Agent (Nous Research)?

Answer:

Hermes has three layers for "custom instructions," each with a different scope. For your use case (multiple projects, AI-native tooling, you already run `ww`/`iclaw`/`zz`), you'll likely want all three.

**1. `SOUL.md` — global persona / always-on instructions**

This is the top-level system prompt slot — persistent across every session, every project, until you switch profiles.

```bash
$HERMES_HOME/SOUL.md   # default: ~/.hermes/SOUL.md
```

SOUL.md sits at the top level of the system prompt and becomes the agent's identity itself. Edit it directly:

```bash
cat ~/.hermes/SOUL.md
# then edit with your editor of choice
$EDITOR ~/.hermes/SOUL.md
```

A minimal template, per the docs: "You are a pragmatic senior engineer with strong taste. You optimize for truth, clarity, and usefulness over politeness theater." — reword to your own voice (e.g. "prefer first-principles explanations, show code before prose, redact secrets/IPs/tokens by default").

Start a new session after making changes for them to take effect — the system prompt is assembled once at session start and doesn't mutate mid-conversation, for prompt-cache stability.

**2. `AGENTS.md` — project-scoped rules**

Drop this at the root of a repo for repo-specific instructions (coding conventions, redaction rules, deploy procedure, whatever). Place AGENTS.md in the root of the project you are working on and describe project-specific rules. This is loaded alongside SOUL.md when Hermes runs in that directory — think of it as CLAUDE.md's equivalent.

**3. Profiles — fully isolated agents with separate instructions**

Given you want a designer/programmer/researcher-style split (your `ww`/`iclaw`/`zz` setup already hints at this), profiles let each have its own `SOUL.md`, skills, memory, and API keys:

```bash
hermes profile create work --clone        # copy config/SOUL.md/.env only
hermes profile create backup --clone-all  # + memory + skills + sessions
```

Command aliases are auto-generated — a profile named 'work' gives you `work chat`, `work setup`, `work gateway start`, `work skills list` directly.

**Config-level instructions (`config.yaml`)**

Model routing, terminal backend, self-learning toggle — not "instructions" per se but shapes behavior:

```bash
hermes config edit
```

**Recommended sequence** (from the official customization guide): 1. Edit SOUL.md and start a new session. 2. Configure config.yaml (model, terminal backend, self-learning). 3. Create AGENTS.md per project. 4. Split roles into profiles with separate SOUL.md files. 5. Accumulate skills — instruct the agent to "make this procedure a skill" after complex tasks. 6. Periodically review MEMORY.md/USER.md for outdated info.

**One gotcha worth knowing**: two other memory files auto-populate and get injected into every session's system prompt — MEMORY.md (2,200 char max) for environment/project conventions, and USER.md (1,375 char max) for your profile — name, communication preferences, skill level, things to avoid. These are agent-curated (it writes to them itself), but you can hand-edit them too — they behave like a lower-priority, auto-updating SOUL.md.

If you want redaction behavior (passwords, IPs, team IDs) to be a standing rule rather than something you repeat per-prompt, put it in `SOUL.md` — that's the only layer guaranteed to load on every single session regardless of project or profile.

References:

- [Hermes Agent Complete Customization Guide](https://note.com/zephel01/n/n95cb081e42de?hl=en)
- [Hermes Agent Masterclass — memory layers](https://www.dailydoseofds.com/p/hermes-agent-masterclass/)
- [Hermes Agent Docs — Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)
