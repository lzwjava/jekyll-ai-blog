---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kali Linux Boot Error Recovery
translated: false
type: note
---

**Question:** The screen is stuck on these errors and not progressing — what should I do next?

**Answer:**

The screen appears **frozen/stuck** after the last `Get:5` line. The system is booting but the desktop isn't loading. Here's what to do step by step:

---

**Step 1: Wait 2–3 minutes first**
Sometimes Kali recovers and loads the desktop slowly after these errors. Just wait.

---

**Step 2: If still stuck, press `Ctrl + Alt + F2`**
This switches to a text terminal. Then run:
```bash
# Login with your credentials, then:
sudo fsck -y /dev/sdb4
sudo reboot
```

---

**Step 3: If you can't type anything — force reboot**
Hold power button 5 seconds → restart → at the **Kali GRUB boot menu**:
1. Highlight your Kali entry
2. Press **`e`** to edit boot options
3. Find the line starting with `linux`
4. Add at the end of that line:
```
systemd.unit=rescue.target
```
5. Press `Ctrl + X` to boot into rescue mode
6. Run:
```bash
fsck -y /dev/sdb4
reboot
```

---

**Step 4: Nuclear option — Recreate the persistence partition**

If `fsck` keeps failing, the persistence partition is too corrupted. Recreate it:
```bash
# WARNING: This erases your persistence data
sudo mkfs.ext4 -L writable /dev/sdb4
```

---

**Which step are you stuck at?** — Does the system eventually show a login screen, or is it completely frozen?

---

**References:**
- [Kali Linux persistence troubleshooting](https://www.kali.org/docs/usb/usb-persistence/)
- [Linux rescue mode via GRUB](https://wiki.archlinux.org/title/GRUB#Boot_into_rescue_mode)
- [e2fsck man page](https://man7.org/linux/man-pages/man8/e2fsck.8.html)
