---
audio: false
generated: true
image: false
lang: en
layout: post
title: Meta Skills and the Skill Creator
translated: false
type: note
---

**Question:** What is a "meta skill" and what is the "skill-creator" skill in this environment?

**Answer:**

## Meta Skill

A **meta skill** is a skill about skills — instead of teaching you *how to do X*, it teaches you *how to create/improve/evaluate skills that do X*.

In this environment's skill system, skills are structured `.md` files that give Claude task-specific instructions (e.g., how to create a `.docx`, how to read a PDF). A meta skill operates one level up: it governs the **skill creation and improvement process itself**.

## The `skill-creator` SkillHere's what you need to know

## Meta Skill — Concept

A **meta skill** operates one level of abstraction above regular skills. Regular skills teach Claude *how to do a task* (make a `.docx`, read a PDF, design a UI). A meta skill teaches Claude *how to create, evaluate, and improve the skills themselves*.

The analogy from ML: a skill is a model, a meta skill is the training loop + evaluation harness for that model.

## `skill-creator` — What It Actually Does

It's the one meta skill in this environment. It implements a full **skill engineering loop**:

```
define intent → draft SKILL.md → write test cases → run evals → review outputs → iterate → package
```

Concretely it covers:

**1. Skill authoring** — Structured `SKILL.md` files with YAML frontmatter (`name`, `description`) + markdown instructions. Three-layer progressive disclosure: metadata (always in context) → SKILL.md body (on trigger) → bundled resources (on demand).

**2. Triggering optimization** — The `description` field in frontmatter is the *primary mechanism* by which Claude decides to use a skill. The skill-creator runs a `run_loop.py` optimization script that A/B tests descriptions against a 60/40 train/test eval split, iterating up to 5 times to maximize trigger rate without overfitting.

**3. Eval harness** — Writes `evals.json`, runs test prompts, grades outputs via assertion checking, and generates an HTML review viewer (`generate_review.py`) for human feedback before the next iteration.

**4. Packaging** — `package_skill.py` bundles the final skill into a `.skill` file for installation.

## Skill File Structure

```
my-skill/
├── SKILL.md           ← required; YAML frontmatter + instructions
└── (optional)
    ├── scripts/       ← executable code for deterministic steps
    ├── references/    ← docs loaded into context as needed
    └── assets/        ← templates, fonts, icons
```

## Why It Matters for You

Since you build CLI agents and automation tools (`ww`, `iclaw`, `zz`), the skill system is essentially **prompt engineering with version control and evals**. The skill-creator gives you a reproducible loop for shipping reliable Claude behaviors — same philosophy as iterating on a fine-tuned model but at the prompt layer. You could author skills for your own workflows (e.g., a skill for auto-generating your blog posts in your style, or a skill for structured code review against your bank's engineering standards) and use skill-creator to tune and test them systematically.
