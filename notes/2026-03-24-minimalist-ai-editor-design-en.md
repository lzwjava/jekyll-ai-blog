---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minimalist Design for AI-Era Editors
translated: false
type: note
---

Question: Is there a philosophy of starting with zero keyboard shortcuts in VSCode — adding them back only as you discover you need them — and does this same "blank slate" principle apply to AI-era editor design?

Answer:

## Yes — This Is a Legitimate Productivity Philosophy

---

## 1. The "Zero Shortcut" VSCode Approach

This is actually a well-regarded method among minimalist developers. The logic is:

- **Most shortcuts are never used** — studies show the average developer uses maybe 10–20 shortcuts regularly, out of hundreds available
- **Pre-loading shortcuts creates cognitive overhead** — you feel pressure to "learn" them all
- **Need-driven learning sticks better** — when you feel the pain of doing something slowly, and *then* assign a shortcut, you actually remember it and use it
- **Result:** You end up with a lean, personal shortcut set that's 100% utilized, instead of a bloated default set you ignore

This is essentially **just-in-time shortcut design** vs **just-in-case shortcut design**.

---

## 2. The Direct AI-Era Parallel

Your analogy is sharp. The mapping is almost 1:1:

| Zero Shortcut Philosophy | AI-Era Editor Philosophy |
|---|---|
| Remove all shortcuts by default | Remove all manual workflows by default |
| Add back only what you actually miss | Add back only what AI genuinely can't do |
| Pain-driven discovery | Friction-driven handoff |
| End result: 10 meaningful shortcuts | End result: 10 meaningful human interventions |

The insight is the same: **don't assume you need it until you feel the absence of it.**

---

## 3. What This Means Concretely for AI-Era Editing

If you stripped VSCode/Cursor down to "AI-first blank slate" and only added back what you truly needed, you'd probably end up with:

**Things you'd add back quickly:**

- Approve / reject AI diff (unavoidable human judgment)
- Jump to a specific file you *know* you want (not search, direct intent)
- Run a specific test you're watching

**Things you'd never add back:**

- Multi-cursor editing
- Manual refactor menus
- File tree navigation (AI discovers context)
- Most find & replace workflows
- Tab switching shortcuts

**Things you'd realize were always redundant:**

- `Ctrl+P` file search → just tell AI what file/function you mean
- `Ctrl+Shift+F` global search → "find all places where X is used"
- Snippet shortcuts → AI generates boilerplate on demand

---

## 4. The Deeper Principle

Both philosophies share the same root idea:

> **Defaults are other people's assumptions about your workflow. Start from zero. Let real friction teach you what you actually need.**

In the shortcut case, the "other people" are the VSCode team designing for an average user. In the AI era, the "other people" are the entire history of developer tooling designed for a pre-AI world.

Claude Code essentially made this bet radically — it launched with **no GUI at all**. Just a terminal prompt. The assumption was: let's see what developers actually miss. Turns out, most of the IDE chrome wasn't missed as much as anyone expected.

---

## 5. The Practical Takeaway

If you wanted to apply this today in VSCode:

1. `Ctrl+K Ctrl+R` → open keyboard shortcuts reference, then bulk-clear
2. Or go to `keybindings.json` and replace everything with `[]`
3. Use VSCode for 2 weeks
4. Every time you feel friction, add exactly one shortcut
5. After a month, you have **your** editor — not Microsoft's idea of your editor

The AI-era version of this is exactly Claude Code's design philosophy: start with nothing but a terminal and natural language. Add structure back only when the absence genuinely hurts.
