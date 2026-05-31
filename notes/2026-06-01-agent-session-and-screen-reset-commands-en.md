---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agent Session and Screen Reset Commands
translated: false
type: note
---

From the Hermes Agent docs:

- `/reset` (alias `/new`): Starts a fresh session. Clears conversation history and gives you a clean slate, but keeps the terminal screen as-is.

- `/clear`: Clears the screen AND starts a new session. It's essentially `/reset` + clearing the terminal display.

Both create a new session. The only difference is that `/clear` also wipes the visible terminal output so you start with a clean screen.

Note: tool changes (enabling/disabling toolsets) take effect on `/reset` — they don't apply mid-conversation because that would break prompt caching.