---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI-Native IDE for Code Inspection
translated: false
type: note
---

Question: Should tools like Claude Code or OpenCode support a direct “/read @file” style command so users don’t need to switch to VSCode to inspect file contents?

Answer:

Yes — that kind of `/read @file` or “inline file viewing” experience is exactly what improves the flow you’re pointing at.

What you’re noticing is a **context-switch friction problem**:

* You ask the AI to work on a codebase
* But then you still have to open VSCode (or another editor) to verify files
* That breaks the “closed loop” feeling of working inside one system

A better integrated design would look like:

### 1. First-class file read in the AI interface

Instead of:

```
show me marp_watch.py
```

You’d have:

```
/read @ww/marp/marp_watch.py
```

Or even:

```
@ww/marp/marp_watch.py
```

This makes the file itself a *referenceable object*, not just a string argument.

---

### 2. Why this matters

This is not just convenience — it changes the workflow:

* **Fewer context switches** → less cognitive load
* **Stronger AI grounding** → model always sees exact file state
* **Faster iteration loop** → read → modify → verify inside same environment
* **Better reproducibility** → no ambiguity about “which file version”

---

### 3. Why current systems still rely on editors

Tools like Claude Code or similar setups often rely on VSCode because:

* Editors are already optimized for file navigation
* AI tools initially focused on *generation*, not *navigation UX*
* File browsing UI is non-trivial (tree views, diff views, search, etc.)

But this is changing — newer agent-style workflows are clearly moving toward:

> “AI as the primary IDE surface, editor becomes optional”

---

### 4. What a smoother system would feel like

A truly integrated experience would include:

* `/read @file`
* `/search "pattern"`
* `/diff @file`
* `/edit @file`
* inline previews (no external editor needed)

At that point, VSCode becomes just one possible renderer, not the center of workflow.

---

### Bottom line

Yes — your intuition is correct.
A `/read @file` style command (or equivalent entity-based file reference) is a key step toward a more seamless “AI-native IDE” where you don’t need to jump to VSCode just to inspect state.

The real direction is: **files should behave like addressable objects inside the conversation, not external artifacts you go fetch.**
