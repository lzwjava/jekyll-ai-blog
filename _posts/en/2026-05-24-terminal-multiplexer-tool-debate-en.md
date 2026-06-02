---
audio: false
generated: true
image: false
lang: en
layout: post
title: Terminal Multiplexer Tool Debate
translated: false
type: note
---

**Question:** What do you think about this conversation (with names hidden)?

**Answer:**

This is a classic "terminal multiplexer religion war" conversation among experienced developers. Here's what's actually going on:

**The core tension:** Everyone has the same problem — managing many terminal sessions across different working directories — but nobody agrees on the right tool.

**The positions in play:**

- **Person A** uses Warp as a terminal *manager* (left-panel directory nav), not for its AI agent features. Smart repurposing of a tool.
- **Person B** finds Warp's agent unusable, prefers Hermes + Claude Code. Relatable — Warp's agent is mediocre compared to Claude Code.
- **Person C** went to 17 Ghostty windows and "completely crashed" — the chaos state everyone hits before adopting a real multiplexer.
- **Person D** uses one Ghostty window as a controller to manage the others — basically reinventing tmux manually.
- **tmux objection raised:** logs don't scroll back far enough in tmux. This is a real pain point (scrollback buffer limits), solvable with `history-limit 50000` in `.tmux.conf` but many don't know that.

**What I actually think:**

The conversation reveals a gap between what these tools *market themselves as* (AI agents, smart terminals) and what experienced devs actually use them for (session management, log tailing, directory jumping).

Warp's killer feature isn't the agent — it's the left-panel session tree. That's just a GUI tmux. The people saying "I can't figure out the agent" are probably right to ignore it.

For your setup specifically, Zhiwei — you're already on Claude Code, which is the correct agent. What you'd benefit from is clean session management. `tmux` + `tmuxinator` with named sessions per project beats 17 Ghostty windows. Or just use Warp's session tree and ignore everything else it tries to sell you.

**The iOS jailbreak plugin nostalgia** at the end is just old-timers recognizing each other — irrelevant to the tooling debate but human.
