---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows Fast Startup Causes EXT4 Error
translated: false
type: note
---

**Question:** After switching to a different SSD, why am I still getting the same EXT4 journal inode error?

**Answer:**

This new screenshot reveals a **critical new clue** at the very top:

```
The disk contains an unclean file system (0, 0).
The file system wasn't safely closed on Windows. Fixing.
```

**This tells us the real root cause — it's NOT the SSD hardware.**

---

**What's actually happening:**

The problem is your **Kali Linux persistence partition** (`sdb4`, labeled `writable`) is being **accessed by Windows before Linux boots**. Windows touches the EXT4 partition (which it can't properly handle), leaves it in a "dirty" state, and then Kali fails to mount it cleanly.

This happens when:
- You're dual-booting Windows + Kali
- **Windows Fast Startup / Hibernate is enabled** — Windows doesn't fully shut down, it hibernates the disk state, causing the "unclean" flag

---

**Fix — Disable Windows Fast Startup:**

1. Open Windows → **Control Panel → Power Options**
2. Click **"Choose what the power buttons do"**
3. Click **"Change settings that are currently unavailable"**
4. **Uncheck** "Turn on fast startup"
5. Click Save → **Full shutdown** Windows (not restart)
6. Boot into Kali again

**Also run fsck from a live session:**
```bash
sudo fsck -y /dev/sdb4
```

---

**Why a new SSD didn't help:** The issue is in the **software/OS interaction**, not the disk hardware itself.

---

**References:**
- [Disable Windows Fast Startup for dual boot](https://help.ubuntu.com/community/WindowsDualBoot#Fast_Startup)
- [EXT4 unclean filesystem fix](https://wiki.archlinux.org/title/Fsck)
- [Kali Persistence setup guide](https://www.kali.org/docs/usb/usb-persistence/)
