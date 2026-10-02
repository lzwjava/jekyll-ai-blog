---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote Proxy Functions Copied
translated: false
type: note
---

All set! The functions from your local `~/.zprofile` have been copied to the remote machine's `~/.profile` and `~/.bashrc`.

Now on the remote machine you can use:

| Command | Action |
| --------- | -------- |
| `start_proxy` | Turn proxy ON → `http://127.0.0.1:7890` |
| `stop_proxy` | Turn proxy OFF |
| `start_proxy_without_prefix` | Proxy without `http://` prefix |
| `start_git_proxy` | Set git proxy |
| `stop_git_proxy` | Unset git proxy |
| `checkproxy` | Show current proxy settings |

They'll be available on next login, or `source ~/.profile` to use right now.
