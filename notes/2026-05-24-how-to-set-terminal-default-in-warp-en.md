---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Set Terminal Default in Warp
translated: false
type: note
---

Ah got it! You want the left sidebar in Warp to show only terminal sessions, not agent sessions. Let me check the current Warp settings for this.Got it clearly now. You want new tabs in the left sidebar (vertical tabs) to default to **terminal mode**, not agent mode. Here's exactly how:

**Settings > Features > General → change "Default mode for new sessions" to Terminal.**

Terminal mode is the default when you open a new tab or pane — it looks and behaves like a traditional terminal with agent controls not always visible. If yours is currently set to Agent, go to **Settings > Features > General** and change **"Default mode for new sessions"** to **Terminal**.

Then with vertical tabs on, every new tab in the left sidebar will be a plain terminal session, not an agent conversation.

And if you want to make it permanent in the config file directly:

```toml
# ~/.warp/settings.toml  (or wherever your Warp config lives)
[features]
default_session_mode = "terminal"
```

When you do need an agent tab, you can still open one on demand via the `+` menu in the vertical tabs panel — it lets you choose Agent, Terminal, or Cloud agent explicitly. So you get terminal by default, agent when you want it. Best of both.