---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code CLAUDE.md Files Merge Together
translated: false
type: note
---

Question: When both a project-level `CLAUDE.md` and a global `~/.claude/CLAUDE.md` exist, will both take effect or only the project-level one?Answer:

**Both take effect simultaneously** — they are merged, not mutually exclusive.

### How it works

Claude Code reads both files when you start a session inside a project folder. The global file loads first, then the project-level file layers on top of it. So if your global file says "always explain things step by step" and your project file says "this site uses WordPress with a custom theme," Claude will do both.

### Load order & priority

When you launch Claude Code, it walks up the directory tree from wherever you run `claude`, loading every `CLAUDE.md` it finds along the way. Every ancestor directory gets checked. Instructions merge together, with closer files taking priority over distant ones.

The priority stack (highest → lowest):

```
Project CLAUDE.md          ← highest priority
Parent directory CLAUDE.md
...ancestor directories...
~/.claude/CLAUDE.md        ← lowest priority (global)
```

### Conflict resolution

If the same instruction appears at multiple levels, the more specific tier wins. For example: Global says "Use 2-space indentation", Project says "Use 4-space indentation" — the project wins for that project.

### Practical mental model

Your global file is where you put the things that make Claude feel like it already knows you — your preferences, your style, your working habits. Your project-level files are where you put the things that make Claude effective inside a specific codebase. If the information is about **you**, it goes in global. If the information is about the **project**, it goes in the project folder.

### Summary

| File | Scope | Use for |
|------|-------|---------|
| `~/.claude/CLAUDE.md` | All projects | Personal style, coding principles, global rules |
| `./CLAUDE.md` (project) | This project only | Tech stack, architecture, project-specific rules |

So your global coding principles (like the ones from Wang Yin's rules) are perfect for `~/.claude/CLAUDE.md`, while project-specific context (e.g. "this uses Next.js + Prisma") belongs in the project-level file.

References:

- [Claude Code Memory Files: Global vs Project Level](https://raythanni.substack.com/p/claude-code-memory-files-global-vs)
- [CLAUDE.md Files and Memory Hierarchy](https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/4.1-claude.md-files-and-memory-hierarchy)
- [Mastering CLAUDE.md: Multi-Project Workflows](https://www.shahabpapoon.com/blog/mastering-claude-md-multi-project-workflow/)
