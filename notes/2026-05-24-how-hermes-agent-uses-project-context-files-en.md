---
audio: false
generated: true
image: false
lang: en
layout: post
title: How Hermes Agent Uses Project Context Files
translated: false
type: note
---

Now I have a clear picture. Here's how AGENTS.md works as per-project rules in hermes-agent:

---

## How AGENTS.md Works in Hermes Agent

There are TWO injection points for per-project context files:

### 1. Startup: System Prompt Injection

When you launch `hermes` in a directory, `agent/prompt_builder.py::build_context_files_prompt()` runs at startup. It scans the CWD for project context files in priority order (first found wins):

    1. .hermes.md / HERMES.md  (walks up to git root)
    2. AGENTS.md / agents.md   (cwd only)
    3. CLAUDE.md / claude.md   (cwd only)
    4. .cursorrules             (cwd only)

Only ONE of these is loaded into the system prompt (capped at 20,000 chars). The found content gets wrapped with a header "# Project Context — The following project context files have been loaded and should be followed" and injected into the `context` slot of the system prompt.

Independent of all of this, `~/.hermes/SOUL.md` (your global identity/personality) is always loaded separately into the `stable` slot.

### 2. Runtime: Subdirectory Hint Discovery

This is the clever part. `agent/subdirectory_hints.py` implements a `SubdirectoryHintTracker` that watches tool calls as they happen. When the agent navigates into a subdirectory (via `read_file`, `terminal`, `search_files`, etc.), the tracker:

1. Extracts the target directory from the tool arguments
2. Walks up to 5 ancestor levels looking for AGENTS.md / CLAUDE.md / .cursorrules
3. On first visit to a directory, loads any found hint files (capped at 8,000 chars each)
4. Appends the hint text to the tool result — NOT the system prompt

This means: if `project/AGENTS.md` has top-level rules, and `project/backend/AGENTS.md` has backend-specific rules, the agent gets the backend rules at the moment it starts working in `backend/` — without modifying the system prompt (preserving prompt caching).

### How You Use It

Put an `AGENTS.md` in your project root. Example from hermes-agent itself (the one you're looking at right now):

    hermes-agent/AGENTS.md   ← project-level rules

Content you'd typically include:
- Development environment setup (venv, dependencies)
- Project structure overview
- How to add tools / commands
- Testing conventions
- Commit conventions
- Key architectural decisions

### The --ignore-rules Flag

If you want to skip all context file loading (for batch processing, data generation, etc.):

    hermes --ignore-rules
    # or: HERMES_IGNORE_RULES=1 hermes

This sets `skip_context_files=True` and `skip_memory=True` on the AIAgent.

### Summary of the Flow

    Session start:
      CWD/AGENTS.md → system prompt "context" slot (once, at startup)
      ~/.hermes/SOUL.md → system prompt "stable" slot (always)

    During conversation:
      Agent calls read_file("backend/src/main.py")
        → tracker sees "backend/src/" is new
        → scans backend/src/, backend/, project root for hint files
        → appends any found AGENTS.md content to the tool result
        → marks directory as loaded (won't repeat)

The design preserves prompt caching (system prompt doesn't change mid-conversation) while still giving the agent project-specific context exactly when it needs it.