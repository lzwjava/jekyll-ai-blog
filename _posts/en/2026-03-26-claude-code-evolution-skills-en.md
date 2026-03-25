---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Evolution of Claude Code Skills
translated: false
type: note
---

Question: What is the history of “skills” in Claude Code?

Answer:

The **Skills** system in Claude Code evolved through **three major phases**: hidden internal capability → community hacks (Superpowers) → official platform feature.

---

# Phase 0 — Before Skills (Prompt-only era)

**Time:** early Claude Code (≈ v1.0)
Claude Code originally worked purely via prompts:

* you tell it what to do
* it generates code directly
* no reusable behaviors
* no persistent workflows

This caused:

* inconsistent outputs
* no standard engineering process
* repeated prompting every task

So users began hacking **structured prompts** manually.

---

# Phase 1 — Hidden internal “skills” discovered

Developers noticed Claude Code already had **undocumented support** for skill files.

A blog describing the discovery states:

* Claude Code had a **hidden skills system**
* supported `SKILL.md` files
* may have existed as early as **Claude Code 1.0**
* but not officially documented yet ([blog.fsck.com][1])

This means:

> Skills existed internally before being released publicly.

---

# Phase 2 — Community-built skills (Superpowers era)

Before official release, developers created their own system.

The most influential one:

* Superpowers
* created by Jesse Vincent
* implemented skill loading
* structured workflows
* multi-agent development

Early installation was hacky:

* fetch `SKILL.md`
* modify `~/.claude/CLAUDE.md`
* teach Claude to load skills manually ([blog.fsck.com][2])

This period introduced:

* brainstorming skill
* TDD skill
* code review skill
* debugging skill
* git workflow skill

This basically invented **Claude skill-based programming**.

---

# Phase 3 — Official Anthropic Skills launch (Oct 2025)

Anthropic officially released **Claude Skills**:

* reusable modules
* auto-triggered behaviors
* custom workflows
* shared across Claude apps and API ([The Verge][3])

Skills became:

* folder-based
* `Skill.md`
* metadata + instructions
* optional scripts

They function like:

> mini-agents inside Claude

---

# Phase 4 — Plugin + marketplace ecosystem

After official launch:

* skills directory
* skill marketplaces
* auto-activating skills
* enterprise skills
* community libraries

Example:

* 200+ skills available
* UI design skills
* PDF skills
* coding skills
* workflow skills ([Claude Code Agents][4])

Skills became:

* composable
* shareable
* versioned
* auto-detected

---

# Phase 5 — Superpowers becomes official plugin (2026)

Superpowers later became:

* official marketplace plugin
* structured dev workflow
* multi-agent coding
* TDD enforced pipeline ([Pasquale Pillitteri][5])

Now skills are used for:

* planning
* coding
* testing
* reviewing
* merging

---

# Final Evolution Timeline

```
Prompt-only Claude
        ↓
Hidden skill support (undocumented)
        ↓
Community hacks (Superpowers SKILL.md)
        ↓
Official Skills launch (Anthropic)
        ↓
Plugin ecosystem
        ↓
Auto-triggering agent workflows (today)
```

---

# Why Skills Matter

Skills changed Claude Code from:

Before:

```
Prompt → code
```

After:

```
Prompt → skill → workflow → subagents → code
```

This is why modern Claude Code feels like:

* senior engineer
* not autocomplete
* structured developer

---

# Key Insight

Skills = **Reusable agent behaviors**

They are:

* prompt templates
* execution plans
* development methodology
* mini AI agents

---

References:

* [https://blog.fsck.com/2025/10/16/skills-for-claude/](https://blog.fsck.com/2025/10/16/skills-for-claude/)
* [https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents](https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents)
* [https://www.tomsguide.com/ai/claude-just-got-customizable-skills-heres-how-they-could-supercharge-your-workflow](https://www.tomsguide.com/ai/claude-just-got-customizable-skills-heres-how-they-could-supercharge-your-workflow)
* [https://blog.fsck.com/2025/10/27/skills-for-openai-codex/](https://blog.fsck.com/2025/10/27/skills-for-openai-codex/)
* [https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide](https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide)

[1]: https://blog.fsck.com/2025/10/16/skills-for-claude/?utm_source=chatgpt.com "Skills for Claude!"
[2]: https://blog.fsck.com/2025/10/27/skills-for-openai-codex/?utm_source=chatgpt.com "Porting Skills (and Superpowers) to OpenAI Codex"
[3]: https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents?utm_source=chatgpt.com "Anthropic turns to 'skills' to make Claude more useful at work"
[4]: https://www.claudecodeagents.com/skills?utm_source=chatgpt.com "175 Auto-Activating Skills for Claude Code | Trigger Phrases | Claude Code Agents"
[5]: https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide?utm_source=chatgpt.com "Superpowers for Claude Code: Complete Guide 2026"