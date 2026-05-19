---
audio: false
generated: true
image: false
lang: en
layout: post
title: macOS Notification for Hermes Agent Turns
translated: false
type: note
---

That's a **post-LLM-call hook script** for Hermes Agent — it fires a macOS notification every time the agent finishes a turn (the tool-calling loop completes).

Here's what it does step by step:

1. **Reads a JSON payload from stdin** — Hermes passes structured data via `post_llm_call` hook, which includes `cwd` (current working directory), `user_message`, and `conversation_history` count.

2. **Extracts three fields:**
   - The **basename of the working directory** (e.g. `hermes-agent`, `jekyll-ai-blog`)
   - The **first 10 characters of the user's message** (so you can see what the turn was about)
   - The **number of conversation turns** so far

3. **Fires a macOS notification** via `terminal-notifier`:
   - Title: `Hermes Agent — <project-dir>`
   - Subtitle: `msg: <preview>  |  turns: <N>`
   - Body: "Hermes has completed one turn."
   - Plays the `Glass` sound
   - Clicking it brings Ghostty (your terminal) to the foreground
   - Uses a `-group` flag so notifications stack/replace rather than spam

4. **Ends with `printf '{}\n'`** — this is the JSON response the hook system expects (a silent no-op, meaning "everything's fine, don't block").

So every time I finish responding to you, a notification pops up saying something like:

> **Hermes Agent — hermes-agent**  
> msg: what's this  |  turns: 3  
> Hermes has completed one turn.

It's very much a personal productivity / awareness thing — lets you know when the agent is done without staring at the terminal. Cleanly written. Want me to customize it or disable it?