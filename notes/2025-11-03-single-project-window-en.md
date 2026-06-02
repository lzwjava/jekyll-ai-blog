---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Single Window Per Project Benefits
translated: false
type: note
---

Spot on—that's a killer refinement to the window-positioning hack we were riffing on. Sticking to *one* dedicated window (or terminal/VSCode instance) per project/task enforces that "single responsibility" principle without the mental tax of juggling duplicates. It's like giving each project its own little fortress: no intra-project clutter means less chance of scattering focus on sub-tasks (e.g., accidentally flipping between two VSCode tabs for the same backend tweak).

Why it clicks especially for your setup:

- **Reduces Decision Fatigue**: Opening a second window "just in case" invites the trap of "which one has the latest diff?"—boom, instant context slip. One window keeps everything pinned: your AI prompts in the integrated terminal, logs scrolling in the output panel, and code diffs right there. It's pure flow state fuel.
- **Easier Visual Hierarchy**: With your 3-4 window cap, this amps up the spatial cues. Project 1's VSCode stays in that left-half sweet spot, undivided; no splitting hairs on panes unless it's a deliberate debug session.
- **AI Synergy**: For Claude Code runs, one pane per project window means prompts stay contextual—no cross-pollinating ideas between unrelated features.

Quick enforcement hack if you slip into the multi-window habit: Set a VSCode workspace setting (`files.autoSave: "afterDelay"`) to nudge you back to the single instance, or just alias your launcher scripts to always target the existing window (e.g., `code --reuse-window /path/to/project`). I've seen devs swear by this in their dotfiles for keeping things monastic.

Love how you're iterating on this iteratively—feels like your self-taught jam. What's the biggest win you've noticed from capping at one-per-project so far? Or any sneaky scenarios where you've been tempted to double up?
