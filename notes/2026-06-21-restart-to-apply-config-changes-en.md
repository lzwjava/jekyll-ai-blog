---
audio: false
generated: true
image: false
lang: en
layout: post
title: Restart to apply config changes
translated: false
type: note
---

Here's how it works:

**Config is read once at agent creation time.** The `max_tokens` value is set during `init_agent()` and stays for the lifetime of the CLI process.

**What each action does:**

| Action | Re-reads config? | Picks up `max_tokens`? |
| --- | --- | --- |
| `/clear` or `/new` | No — same agent object | No |
| `/model` to different model | Yes — recreates agent | Yes (if you switch away and back) |
| **Ctrl+C + restart** | **Yes — fresh process** | **Yes** |

The agent is only recreated when the route signature changes (model + provider + base_url + api_mode). Editing `max_tokens` in config.yaml doesn't change the signature, so `/clear` won't help.

**TL;DR: Ctrl+C out of the CLI and relaunch.** That's the reliable way.
