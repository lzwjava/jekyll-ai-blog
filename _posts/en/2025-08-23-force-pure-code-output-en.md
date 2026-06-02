---
audio: false
generated: true
image: false
lang: en
layout: post
title: Force Pure Code Output Methods
translated: false
type: note
---

Got it—you want Claude Code (and your “router” workflows that call it) to output **code only**, with **no inline comments/docstrings/explanations**. Here are three reliable ways to enforce that, from softest to strongest. No tables—just straight steps.

---

# 1) Put the rule in `CLAUDE.md` (global or per-project)

Claude Code loads “memory” files automatically and follows them across sessions. Add a short, explicit rule:

**Global (all projects):** `~/.claude/CLAUDE.md`
**Per project (checked in):** `./CLAUDE.md`

```md
# Output rules
- When generating code, output code only.
- Do not include inline comments, block comments, docstrings, or explanatory prose unless I explicitly ask.
- Keep messages concise; if an explanation is needed, put it after the code block and only if I ask.
```

Tip: you can manage these memories with `/memory` and quickly add new ones by starting a message with `#` in Claude Code. ([Anthropic][1])

---

# 2) Make a **custom Output Style** that bans comments (stronger)

Output Styles modify Claude Code’s **system prompt**. Create one and switch to it:

**Create:**

```
/output-style:new I want an output style that always outputs code without any comments or docstrings, no explanations.
```

This creates a file under `~/.claude/output-styles/…`. You can edit it to ensure the rule is unambiguous:

```md
---
name: Code Only (No Comments)
description: Always emit code without comments/docstrings; no explanations unless asked.
---
# Instructions
- You are coding in "code-only" mode.
- Never include inline comments, block comments, or docstrings.
- Do not add prose before or after code unless explicitly requested.

## Specific Behaviors
- If a task implies tests, output the test file(s) as code only.
- If clarification is needed, ask briefly, no explanations.
```

**Activate:**

```
/output-style "Code Only (No Comments)"
```

(Output styles directly change the system prompt; you can switch with `/output-style` anytime.) ([Anthropic][2])

---

# 3) Append an extra system prompt at runtime (strongest / per-session)

If you launch Claude Code from CLI or a script, add:

```bash
claude --append-system-prompt "Always output code only. No inline comments, no block comments, no docstrings, no explanations unless explicitly asked."
```

You can also set this via `/config` if you prefer persistent project settings. (Anthropic notes you can use `--append-system-prompt` to modify Claude Code’s behavior.) ([Anthropic][3])

---

## Where to put “router”-wide rules

* If your “Claude Code router” is just your regular Claude Code sessions across repos, prefer **global memory** (`~/.claude/CLAUDE.md`) or a **custom Output Style** so the rule travels everywhere. ([Anthropic][1])
* If you launch via a script, bake in the `--append-system-prompt` flag so every run inherits the rule. ([Anthropic][3])

---

## Extra guardrails (optional but useful)

* In project memory, add a **“Violations”** line so the model self-checks: “If you are about to output comments/docstrings, stop and remove them.”
* If you sometimes *want* comments, add a one-shot override in your prompt: “This one time, include brief comments.”

That’s it. If you tell me how you start Claude Code (desktop, VS Code, JetBrains, or terminal), I can give you a drop-in snippet for that setup.

[1]: https://docs.anthropic.com/en/docs/claude-code/memory "Manage Claude's memory - Anthropic"
[2]: https://docs.anthropic.com/en/docs/claude-code/output-styles "Output styles - Anthropic"
[3]: https://docs.anthropic.com/en/docs/claude-code/settings "Claude Code settings - Anthropic"
