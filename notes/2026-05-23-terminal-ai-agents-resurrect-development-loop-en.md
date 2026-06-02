---
audio: false
generated: true
image: false
lang: en
layout: post
title: Terminal AI Agents Resurrect Development Loop
translated: false
type: note
---

**Question:** Engineers built OS systems in Emacs, then VS Code, now in terminal/AI agents — is this the right historical arc?

**Answer:**

Close, but the actual arc is more nuanced and interesting:

## The Real IDE Evolution Arc

```
Punchcards / batch jobs (1950s–60s)
    ↓
Terminals + line editors (ed, vi) (1970s)
    ↓
Emacs / full-screen editors (1980s)        ← "living in the editor"
    ↓
IDEs: Turbo Pascal, Visual C++, Delphi (1990s)
    ↓
Eclipse / IntelliJ / heavyweight IDEs (2000s)
    ↓
Sublime Text → Atom → VS Code (2010s)      ← "lightweight + extensions"
    ↓
Terminal-first + AI agents (2020s)          ← we are here
```

## What's Actually True About Each Phase

**Emacs era** — Emacs was less "build OS" and more "OS *is* Emacs." RMS literally ran his life in it — email, shell, compile, debug. It's a Lisp runtime that happens to edit text. This is the peak of "editor as operating environment."

**VS Code era** — LSP (Language Server Protocol) was the real innovation. Decoupled intelligence from the editor. VS Code won because it was Electron (cross-platform fast to ship) + open extension ecosystem + Microsoft distribution muscle.

**Terminal/Agent era** — what's actually happening now:

```
Claude Code / Aider / Cursor
    = LLM with tool use
    + file system access
    + shell execution
    + git awareness
    → the "agent" IS the IDE
```

## The Deeper Pattern

Each transition is about **where intelligence lives**:

| Era | Intelligence location |
|---|---|
| Emacs | In the editor runtime (Lisp) |
| IDE | In the language server / compiler |
| VS Code | Distributed via LSP protocol |
| AI Agent | In the model weights + context window |

The terminal is winning *again* because agents need raw shell access. A GUI is a bottleneck — the model can't click buttons efficiently, but it can absolutely run `bash`, `git`, `curl`, `python`. So the loop becomes:

```
human intent → LLM → tool calls (bash/read/write/search) → diff → human review
```

Claude Code, Aider, and your own `zz`/`ww` tools are exactly this pattern.

## The Meta-Insight

Engineers didn't abandon power — they **compressed the feedback loop**. Emacs → VS Code was about speed of navigation. VS Code → agents is about speed of *intent execution*. You don't describe code you want, you describe *outcomes* you want.

The terminal was never actually dead — it was always the substrate. The agent just made it the primary interface again, with an LLM as the REPL.
