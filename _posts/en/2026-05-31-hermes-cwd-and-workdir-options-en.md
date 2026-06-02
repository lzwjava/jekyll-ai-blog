---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes CWD and Workdir Options
translated: false
type: note
---

Now I have a clear picture. Here's the answer:

---

**CWD affects Hermes in exactly two ways:**

**1. Project context files (AGENTS.md / CLAUDE.md / .cursorrules)**

When Hermes starts, it scans the CWD for these files and injects them into the system prompt. This is the main thing — it's how Hermes knows about a project's structure, conventions, build commands, etc. The tip from the code:

> "Subdirectory AGENTS.md files are discovered progressively as the agent navigates into folders."

So even within a session, if the agent `cd`s into a subdirectory that has its own AGENTS.md, it gets loaded.

**2. Terminal tool CWD (via TERMINAL_CWD env var)**

The `terminal.cwd` config maps to `TERMINAL_CWD`, which sets where shell commands execute. This is what makes `git status`, `python test.py`, etc. run in the right place.

---

**Do you really need to change dir?**

No. You have three better options from your current session:

1. **`workdir` on terminal commands** — I can run any command with `workdir=~/projects/git-credential-manager` right now. Same effect.

2. **`--ignore-rules` flag** — If you want a clean session without any AGENTS.md, use `hermes --ignore-rules`.

3. **Cron jobs with `workdir`** — For recurring tasks, the `workdir` parameter on cron jobs does exactly this: sets TERMINAL_CWD and loads context files from that directory.

The "open a new tab and cd" advice is only needed if you want a **full interactive session** permanently scoped to that project (autocomplete, context files, all terminal commands defaulting there). For quick inspection or one-off commands, `workdir` on the terminal tool is the same thing without leaving.
