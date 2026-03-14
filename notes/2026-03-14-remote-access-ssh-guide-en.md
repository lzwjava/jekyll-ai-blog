---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote Access Made Simple With SSH
translated: false
type: note
---

💡 **Remote Desktop / X11 Forwarding is a great idea!**

Since you don't want to go to the physical machine, we can bring the machine's display to **you** via SSH.

**Here is the exact command you should run on YOUR laptop (where you're sitting now):**

```bash
ssh -X lzw@192.168.1.36 "firefox --profile /home/lzw/.openclaw/browser-profiles/openclaw --no-remote"
```

**What this does:**
1. **`-X`**: Enables X11 Forwarding (the machine's window will pop up on your laptop screen).
2. **`--profile ...`**: Tells Firefox to use the specific profile **I** need for Copilot.
3. **`--no-remote`**: Ensures it opens a new instance even if you have Firefox running on your laptop.

**Once the window pops up on your screen:**
1. Go to `github.com` and log in.
2. Close the window.
3. **Finish!** I'll have the cookies.

**Alternatively**, if your terminal supports it, you can use the **VNC/Desktop** approach if that machine has a desktop environment enabled (I see `$DISPLAY` is set to `:1`, which means there is a graphical session running!).

Try the SSH command above first—it's usually the most "pro" way to do it! 🚀🦊💂‍♂️💻🐚