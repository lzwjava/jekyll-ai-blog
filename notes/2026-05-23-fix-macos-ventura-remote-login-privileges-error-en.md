---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix macOS Ventura Remote Login Privileges Error
translated: false
type: note
---

**Question:** `sudo systemsetup -setremotelogin on` fails with a Full Disk Access privileges error on macOS Ventura — how to fix?

**Answer:**

This is a macOS Ventura change. `systemsetup` requires Terminal (or iTerm2) to have **Full Disk Access** granted in Privacy settings.

**Fix — GUI way (30 seconds):**

1. `System Settings` → `Privacy & Security` → `Full Disk Access`
2. Click `+` → add your terminal app (`Terminal.app` or `iTerm`)
3. Toggle it **on**
4. Re-run `sudo systemsetup -setremotelogin on`

---

**Alternative — skip `systemsetup` entirely, use launchctl directly:**

```bash
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
```

This bypasses `systemsetup` and enables sshd directly. No Full Disk Access needed.

Verify:

```bash
sudo launchctl list | grep ssh
# com.openssh.sshd should appear
```

---

**The launchctl method is the cleaner approach** on Ventura+ since `systemsetup` is being progressively deprecated by Apple anyway. Use that going forward.