---
audio: false
generated: true
image: false
lang: en
layout: post
title: Evolution of Claude Code Skills Timeline
translated: false
type: note
---

Question: What is the timeline of the “skills” system in Claude Code, with the time of each phase?

Answer:

Here is the **chronological timeline** of how **Claude Code skills** evolved, including approximate dates for each phase.

---

# Phase 0 — Prompt-only Claude Code

**Time:** Early–mid 2024
**State:** No skills system exposed

Characteristics:

* Only direct prompting
* No reusable workflows
* No modular behavior
* No structured engineering pipeline

Typical usage:

```
Prompt → Claude → Code
```

Limitations:

* inconsistent outputs
* repeated instructions
* no reusable expertise

---

# Phase 1 — Hidden internal skills support (undocumented)

**Time:** Late 2024 (approx. Q4 2024)

Developers discovered:

* Claude Code could read **SKILL.md**
* hidden modular instruction loading
* internal reusable behaviors
* not officially documented

This indicates **skills existed internally first**, before release.

What people noticed:

* folder-based instructions worked
* Claude reused behavior automatically
* skills looked like “mini agents”

---

# Phase 2 — Community skills (Superpowers era)

**Time:** Early–mid 2025

Developers created external skill loaders, especially:

* Superpowers
* community skill libraries
* manual injection into Claude config

This introduced:

Common skills:

* brainstorming
* code review
* TDD
* debugging
* git workflows
* verification

This is when **skill-based development became popular**.

Pipeline became:

```
Prompt → Skill → Claude → Code
```

---

# Phase 3 — Official Claude Skills announcement

**Time:** October 2025

Anthropic officially introduced **Claude Skills**:

Features:

* reusable modules
* skill folders
* metadata
* auto activation
* shareable skills

Skills became:

```
.skills/
  brainstorming/
  code-review/
  tdd/
```

Claude could:

* detect skills
* auto choose skills
* chain skills

This turned Claude into **workflow-based agent**.

---

# Phase 4 — Skills ecosystem expansion

**Time:** Late 2025 (Nov–Dec 2025)

What emerged:

* skill libraries
* skill marketplaces
* team-shared skills
* domain skills
* UI skills
* infra skills

Organizations started creating:

* company engineering skills
* release pipeline skills
* architecture skills

Claude became:

```
Agent runtime + skill modules
```

---

# Phase 5 — Plugin-based skills (Superpowers integration)

**Time:** Early 2026

Skills moved to:

* plugin systems
* installable skill packs
* `/skills` command
* skill discovery
* skill metadata

Example (what you saw):

```
Skills
14 skills

verification-before-completion
receiving-code-review
brainstorming
using-git-worktrees
```

Now skills are:

* installable
* composable
* versioned
* plugin-provided

---

# Complete Timeline

```
Early 2024
Prompt-only Claude Code
(no skills)

Late 2024
Hidden internal skills discovered

Early 2025
Community skills (Superpowers)

Oct 2025
Official Claude Skills released

Late 2025
Skills ecosystem grows

Early 2026
Plugin-based skills (/skills command)
```

---

# Evolution of Claude Code

| Stage      | Behavior                                     |
| ---------- | -------------------------------------------- |
| 2024       | prompt → code                                |
| late 2024  | prompt → hidden skill → code                 |
| 2025 early | prompt → community skill → code              |
| 2025 Oct   | prompt → official skill → workflow → code    |
| 2026       | prompt → skill pipeline → multi-agent → code |

---

# Key Insight

Skills turned Claude Code from:

```
code generator
```

into:

```
workflow-driven AI engineer
```

That is why modern Claude Code feels much more structured.

---

References:

* [https://blog.fsck.com/2025/10/16/skills-for-claude/](https://blog.fsck.com/2025/10/16/skills-for-claude/)
* [https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents](https://www.theverge.com/ai-artificial-intelligence/800868/anthropic-claude-skills-ai-agents)
* [https://www.tomsguide.com/ai/claude-just-got-customizable-skills-heres-how-they-could-supercharge-your-workflow](https://www.tomsguide.com/ai/claude-just-got-customizable-skills-heres-how-they-could-supercharge-your-workflow)
* [https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide](https://pasqualepillitteri.it/en/news/215/superpowers-claude-code-complete-guide)
