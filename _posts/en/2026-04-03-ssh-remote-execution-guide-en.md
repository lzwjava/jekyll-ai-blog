---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Remote Execution Guide
translated: false
type: note
---

Sure, here's the review with the IP partially masked:

### What happened

1. **You gave me SSH credentials** — host `213.173.110.xxx`, port 22775, user root
2. **First attempt failed** — no SSH key on the remote, so auth rejected
3. **You manually added the key** via `echo` into `authorized_keys` on the remote
4. **Second attempt succeeded** — connected and pulled the hardware report
5. **Installed emacs-nox** — `apt-get update && apt-get install -y` over SSH, ran in background since it took a while

### How I work

- I run commands **on this server** via shell execution
- For remote machines, I SSH from here — same as any terminal
- Long tasks run in the background, I poll for results when done
- No magic — just `ssh + command` piped through

### The pattern

```
ssh -p <port> root@213.173.110.xxx "command"
```

That's the whole trick. Want to do more on that box, just say the word. 🦞