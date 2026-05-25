---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zed Remote SSH Canonicalization Bug Fixes
translated: false
type: note
---

Found the root cause. From Zed logs:

```
ERROR [worktree] failed to canonicalize root path "/mnt/data/deepseek-v4-inference": 
canonicalizing "/mnt/data/deepseek-v4-inference": No such file or directory (os error 2)
```

The Zed remote server can see the path (it tried to watch it), but fails to **canonicalize** it. This is a known Zed bug with SSH remote. Try these fixes in order:

**Fix 1: Bump inotify limit on remote** (fixes the secondary issue):

```bash
ssh lzw@192.168.1.36 "echo 'fs.inotify.max_user_watches=524288' | sudo tee -a /etc/sysctl.conf && sudo sysctl -p"
```

**Fix 2: Delete the stale remote server and let Zed re-download it**:

```bash
ssh lzw@192.168.1.36 "rm -rf ~/.zed_server/"
```

Then reopen the project in Zed — it will re-upload the server binary.

**Fix 3: Try opening via CLI instead of URL**:

```bash
zed ssh://lzw@192.168.1.36//mnt/data/deepseek-v4-inference/
```

Note the double `//` after the host — some Zed versions need this to correctly parse absolute paths.

**Fix 4: If all else fails, use VS Code Remote SSH as a workaround**:

```bash
code --remote ssh-remote+lzw@192.168.1.36 /mnt/data/deepseek-v4-inference
```

Want me to run Fix 1 + Fix 2 on the remote now?