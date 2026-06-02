---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Lenovo Boot Menu Fix Guide
translated: false
type: note
---

Question: Spam Fn + F12 (or F12) at the Lenovo logo to open the boot menu, but F2 doesn't work?

Answer:

Yes, **Fn + F12** (or just **F12** on some models) is the correct and most reliable key for opening the **one-time boot menu** on Lenovo XiaoXin laptops (and most IdeaPad series). Spam it repeatedly right as the Lenovo logo appears during power-on or restart — timing is key, start pressing before the logo fully shows up.

**F2** (or Fn + F2) is typically for entering the full **BIOS/UEFI setup** menu, not the boot menu. If F2 isn't responding, here are the common reasons and fixes:

### Why F2 Might Not Work
- **Fast Startup in Windows** is enabled (default on Win10/11): This causes "hybrid shutdown" instead of full shutdown, so the firmware skips hotkey detection.
- **HotKey Mode** in BIOS is set in a way that requires Fn for function keys (or vice versa).
- Timing issue: You need to press it very early and repeatedly.
- Some XiaoXin models (e.g., certain 15ARE variants) have known quirks where Windows installers or updates disable F2/F12 hotkeys temporarily.
- Rarely, keyboard/firmware glitch.

### How to Fix and Access BIOS (If You Need It for Secure Boot/CSM Changes)
1. **Disable Fast Startup in Windows** (most common fix):
   - Boot into Windows normally.
   - Go to Settings → System → Power & sleep → Additional power settings → Choose what the power buttons do.
   - Click "Change settings that are currently unavailable" (admin prompt).
   - Uncheck "Turn on fast startup" → Save changes.
   - Shut down completely (not restart).
   - Now power on and spam **F2** or **Fn + F2** at the logo — it should enter BIOS much more reliably.

2. **Full shutdown trick**:
   - From Windows login screen: Hold **Shift** key → click Power → Shut down.
   - This forces a complete power-off.
   - Then power on and spam **F2** / **Fn + F2**.

3. **Novo Button** (if your XiaoXin has one):
   - Many XiaoXin/IdeaPad models have a small pinhole "Novo" button (usually on the side, near power or charging port — looks like a curved arrow).
   - Power off → use a paperclip/SIM tool to press and hold the Novo button → laptop powers on into a special menu.
   - Choose **BIOS Setup** or **Boot Menu** from there.
   - This bypasses keyboard hotkeys entirely and works even if F2/F12 are glitchy.

4. **Other Tips for Boot Menu (Fn + F12)**:
   - If just **F12** alone doesn't work, always try **Fn + F12**.
   - Some models need **Fn lock** toggled (usually Fn + Esc to toggle).
   - Try a different USB port for your Ubuntu drive — some ports detect better.
   - If the boot menu appears but USB options are missing, confirm BIOS changes (Secure Boot off, Boot Mode = Both/UEFI+Legacy) were saved.

Once in BIOS (via any method), make the changes we discussed earlier (disable Secure Boot, set Boot Mode to Both), save/exit (F10 usually), then restart and spam **Fn + F12** to pick the second/lite Ubuntu entry.

If none of this works after trying the Fast Startup disable + full shutdown, your model might need a BIOS update from Lenovo's site (search your exact XiaoXin model number on their Chinese/global support page).

References:

- [https://wiki.archlinux.org/title/Lenovo_XiaoXin_15are_2020](https://wiki.archlinux.org/title/Lenovo_XiaoXin_15are_2020)
- [https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre](https://support.lenovo.com/us/en/solutions/ht104668-how-to-select-boot-device-from-bios-boot-menu-ideapad-thinkpad-thinkstation-thinkcentre-ideacentre)
- [https://support.lenovo.com/us/en/solutions/ht500216-recommended-way-to-enter-bios-ideapad](https://support.lenovo.com/us/en/solutions/ht500216-recommended-way-to-enter-bios-ideapad)
- [https://recoverit.wondershare.com/computer-tips/lenovo-boot-menu-key.html](https://recoverit.wondershare.com/computer-tips/lenovo-boot-menu-key.html)
