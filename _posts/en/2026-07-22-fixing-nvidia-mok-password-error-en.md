---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing NVIDIA MOK Password Error
translated: false
type: note
---

Here's the full picture:

**Current state:**
- `nvidia-driver-580` installed, DKMS modules built ✓
- Secure Boot **enabled** — blocks loading the unsigned module
- MOK key exists at `/var/lib/shim-signed/mok/MOK.der` but **not enrolled**
- You went into MokManager (blue screen), got asked for a password, typed something, got an error

---

## The password thing explained

When you installed `nvidia-driver-580` via apt, Ubuntu's DKMS prompted you to **create a MOK enrollment password** (not your login password). That's the one MokManager is asking for. Two common failures:

1. **You forgot what you typed** — it's a one-time password, easy to forget
2. **Keyboard layout mismatch** — MokManager uses US QWERTY layout. If you set the password thinking you were on a different layout, you'd type the wrong characters

---

## Option A: Recreate the MOK key + password (so you know it)

Run this on the workstation:

```bash
sudo mokutil --reset  # remove old enrollment request
sudo rm /var/lib/shim-signed/mok/MOK.*
sudo dpkg-reconfigure nvidia-dkms-580
```

It will prompt for a **new MOK password** — pick something simple you'll remember (e.g. `1234`). Then reboot:

```
sudo reboot
```

At the blue MokManager screen:
1. **"Enroll MOK from disk"**
2. Navigate to the key → **Continue**
3. **Type the password you just set**
4. **Yes/Confirm**
5. Boot continues → `nvidia-smi` works

---

## Option B: Disable Secure Boot (simpler, no passwords)

From the black POST screen, press **F2** (or Del/F10 depending on your motherboard) to enter BIOS/UEFI settings.

Then find:
- **Security → Secure Boot → Disabled**
- Or **Boot → Secure Boot → Disabled**
- Or **Authentication → Secure Boot → Disabled**

Save and exit (usually **F10**), boot normally. Done — no passwords, no MOK, `nvidia-smi` works immediately.

---

**My recommendation:** Option B. It's one setting, one reboot, zero passwords to remember. Unless you specifically need Secure Boot for security compliance, there's no practical benefit to keeping it on for a dev workstation.

What do you want to do — A (recreate MOK) or B (disable Secure Boot)? If B, I can't navigate the BIOS menu remotely — you'll need to hit F2 during boot and find the setting. But tell me if you get stuck and which motherboard you have, I can look up the exact menu path.