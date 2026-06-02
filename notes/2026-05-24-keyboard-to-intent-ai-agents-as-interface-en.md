---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Keyboard to Intent: AI Agents as Interface"
translated: false
type: note
---

**Question:** Is using AI agents like Hermes/Claude Code to open files (instead of Finder) a good workflow philosophy — minimizing traditional GUI interactions?

**Answer:**

Yes, and you're onto something that compounds over time. Here's the actual principle at work:

## The Keyboard-to-Intent Pipeline

Traditional workflow:
```
thought → Finder/Dock → click → navigate → click → open
```

AI agent workflow:
```
thought → natural language → done
```

The friction reduction isn't just speed — it's **cognitive context switching**. Every time you reach for the mouse or navigate Finder, you're context-switching from *thinking* to *operating*. Claude Code / Hermes keeps you in the thinking layer.

## Why This Scales Better Than Aliases/Scripts

You could alias `open-resume` in your `.zshrc`. But:

```bash
# Traditional: you have to anticipate every command in advance
alias open-resume="open -a Preview ~/projects/.../Zhiwei.Li.Resume.pdf"

# Agent: you don't — fuzzy intent matching handles ambiguity
"open the english resume pdf"  # → agent resolves path, picks right file
```

Agents handle **fuzzy intent** without pre-registration. That's the compounding advantage — every file, every task, zero pre-setup.

## The Real Unlock: Chaining

The reason "open in Preview" as a Claude Code command is more powerful than it looks:

```
# This is just one step in what could be:
"regenerate the PDF, check for LaTeX errors, open it in Preview,
 and if it looks good push to git"
```

Finder can't chain. Scripts can chain but require authoring. Agents chain **on demand, in natural language**, across tools you didn't wire up in advance.

## The Philosophy: GUI as Last Resort

Your instinct matches what Karpathy has articulated — the ideal is:

```
Terminal → Agent → direct API
```

GUI (Finder, browsers for non-research, etc.) = last resort when no programmatic path exists.

The test: *"Could an agent do this if I just described it?"* If yes, don't touch the mouse.

You're essentially building the habit of **treating your computer as an API**, not an application. That's the right direction — and Claude Code is one of the best current interfaces for it.
