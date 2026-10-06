---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS Can't Disable Windows Fast Startup
translated: false
type: note
---

**Question:** How do I disable Fast Startup / Hibernate from the BIOS instead of from within Windows?

**Answer:**

You **cannot disable Windows Fast Startup directly from BIOS** — it's a Windows OS setting. However, you can achieve the same result through BIOS in these ways:

---

**Option 1: Disable Secure Boot (BIOS setting that helps)**
1. Restart → press `Del`, `F2`, or `F12` (depends on motherboard) to enter BIOS
2. Go to **Boot** or **Security** tab
3. Find **Secure Boot** → set to **Disabled**
4. Save & Exit (`F10`)

---

**Option 2: Force proper shutdown via BIOS behavior**
- In BIOS, find **"Fast Boot"** (different from Windows Fast Startup)
- Set it to **Disabled**
- This forces a full POST check each boot, which helps ensure clean disk states

---

**The Real Solution — You Must Do This in Windows:**

Since you can still see the boot messages, Kali **is actually booting**. So:

1. At the Kali login screen, open a terminal
2. Run:
```bash
sudo fsck -y /dev/sdb4
```
3. Reboot

**OR** — Force Windows shutdown without entering Windows:
- Hold **Shift** while clicking Shutdown in the Windows boot menu
- This bypasses Fast Startup and does a full shutdown

---

**Bottom line:** BIOS "Fast Boot" ≠ Windows "Fast Startup". You need to fix it on the Windows side or run `fsck` from Kali directly.

---

**References:**
- [Windows Fast Startup vs BIOS Fast Boot explained](https://www.howtogeek.com/243901/the-difference-between-fast-startup-hibernate-and-sleep-in-windows-10/)
- [fsck manual page](https://man7.org/linux/man-pages/man8/fsck.8.html)
