---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Project Success Guide
translated: false
type: note
---

Question: What is the correct way to use OpenClaw (which uses Claude Code) for sophisticated projects? Should I create a PRD first, and how should I approach complex work incrementally?

Answer:

## Using OpenClaw (Claude Code) Effectively

### What is OpenClaw?
OpenClaw is a wrapper/interface around **Claude Code** — Anthropic's agentic coding CLI. It lets Claude autonomously write, edit, and run code on your machine.

---

### ✅ Your Instinct is Correct — Start with a PRD

Yes, **a good PRD (Product Requirements Document) is the #1 thing** that separates great results from mediocre ones with Claude Code.

**Why PRD matters:**
- Claude Code works best when it has a **clear, structured spec** to follow
- Without a PRD, it will make assumptions and drift from your vision
- A PRD acts as the "source of truth" it can refer back to

**What to include in your PRD:**
```
## Project: Todo App
### Core Features
- Task creation, editing, deletion
- Projects / folders
- Subtasks
- Priority levels (P1-P4)
- Due dates
- Tags/labels

### Tech Stack
- React + TypeScript
- Tailwind CSS
- localStorage / IndexedDB

### UI Reference
- Inspired by: Google Tasks, Linear, Todoist

### Out of Scope (v1)
- Backend sync
- Mobile app
```

---

### 🪜 The Right Workflow

```
1. Write PRD  →  2. Small first task  →  3. Review  →  4. Iterate
```

| Step | What to do |
|------|-----------|
| **1. PRD** | Define scope clearly before touching code |
| **2. Start small** | Ask it to scaffold the project first, not build everything |
| **3. Check output** | Review after each major step |
| **4. Iterate** | Add features one module at a time |

---

### ⚠️ Common Mistakes to Avoid

- **Don't ask for everything at once** — "build a full todo app" leads to messy code
- **Don't skip reviewing** — Claude Code can go in wrong directions silently
- **Don't give vague specs** — "make it sophisticated" is hard to act on vs. "implement drag-and-drop reordering with keyboard shortcuts"
- **Don't let it run too long unattended** — check every 10-15 minutes on complex tasks

---

### 💡 Better Prompt Strategy for OpenClaw

Instead of one giant prompt, break it into phases:

```
Phase 1: "Scaffold the React project with folder structure and routing"
Phase 2: "Build the Task model and CRUD operations"
Phase 3: "Build the sidebar with project navigation"
Phase 4: "Add keyboard shortcuts and search"
Phase 5: "Polish UI and add animations"
```

Each phase = one Claude Code session. **Review before moving to next phase.**

---

### 📋 Recommended First Prompt to OpenClaw

```
Read this PRD carefully before writing any code.
[paste PRD]

Step 1 only: Scaffold the project structure, install dependencies,
and create empty component files with comments describing what
each will do. Do not implement logic yet. Show me the file tree when done.
```

This forces it to **plan before it codes**.

---

### Summary

| Question | Answer |
|----------|--------|
| Is your approach correct? | Mostly yes — but break it into smaller steps |
| PRD first? | **Absolutely yes** |
| Check after some time? | Yes, every 10-15 min for big tasks |
| One big prompt? | No — phase it out |
