---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recovery Mode Missing Network Commands
translated: false
type: note
---

Yes, that's expected—**macOS Recovery** (the mode you're in via startup options or Command-R / power hold on M2) runs a very stripped-down environment to keep it lightweight and secure. Many full-system commands like `networksetup` (located normally at `/usr/sbin/networksetup`) are **not included** in the Recovery partition's PATH or binaries. That's why you get "command not found."

### Quick Confirmation
Run this in your current Terminal to see what's actually available:
```bash
ls /usr/sbin
```
(or `ls /bin`, `ls /usr/bin`) — you'll notice it's a short list compared to normal macOS. No `networksetup` there.

### Workarounds to Clear Proxy Settings
Since we can't use `networksetup` here, here are the best options from this spot:

1. **Best & Simplest: Boot to Safe Mode First (Bypasses Proxy Often)**
   - From Recovery: Choose **Restart** (or force shutdown with power button hold).
   - Immediately hold the **power button** until startup options appear.
   - Select your disk → hold **Shift** → Continue in Safe Mode.
   - Safe Mode loads minimal extensions and often ignores or clears temporary proxy glitches (including Clash leftovers) because third-party kexts/login items don't run.
   - If you reach the desktop/login screen:
     - Open **System Settings > Network > Wi-Fi** (or Ethernet) → Details... → Proxies tab → turn everything **off** (Web Proxy, Secure Web Proxy, SOCKS, Auto Proxy).
     - Or open Terminal normally and run the `networksetup` commands I gave earlier (now available).
   - Then restart normally → the update/setup should proceed without proxy interference.

2. **If Safe Mode Also Hangs: Reinstall macOS from Recovery (Non-Destructive)**
   - In Recovery → choose **Reinstall macOS** (or macOS Tahoe).
   - It downloads and reinstalls the OS files over your existing data/apps (won't erase user files unless it fails badly).
   - During reinstall, it often resets network configs (including proxies) to defaults because it rebuilds system components.
   - Make sure you're on a good Wi-Fi (no proxy needed for Apple's servers ideally—connect to a mobile hotspot if possible to test).
   - This has fixed many stuck-post-update + proxy loops for M-series users.

3. **Advanced Hack: Mount Main Volume & Edit Proxy Plist Directly (If Comfortable with Terminal)**
   In Recovery Terminal:
   ```bash
   diskutil list   # Note your main disk, e.g. disk3s1 or disk1s5 — usually the biggest APFS volume labeled "Macintosh HD" or similar
   diskutil apfs list   # Confirm the volume group
   mkdir /mnt
   mount -uw /Volumes/Macintosh\ HD   # Or whatever your volume is named; use quotes if spaces
   # If mount fails, try: mount -uw /
   cd /Volumes/Macintosh\ HD/Library/Preferences/SystemConfiguration   # This folder holds network prefs
   ls   # Look for com.apple.airport.preferences.plist or preferences.plist
   ```
   - Unfortunately, editing plists properly requires `defaults` command or `plutil`, which may also be missing in Recovery.
   - If `defaults` works (try `defaults read`), you could do something like:
     ```bash
     defaults delete /Volumes/Macintosh\ HD/Library/Preferences/SystemConfiguration/preferences GlobalProxies
     ```
     But this is hit-or-miss—many tools are absent, so it often fails.

   If mounting/editing doesn't work easily, skip to option 1 or 2.

4. **Last Resort: Erase & Clean Install (Data Loss Risk—Backup First if Possible)**
   - If nothing else works and it's truly proxy-stuck forever, from Recovery → Disk Utility → Erase your main volume (APFS) → then reinstall.
   - But try Safe Mode + reinstall first.

Most users in similar stuck-update-with-proxy situations get past it by forcing Safe Mode a couple times or reinstalling. Try booting to Safe Mode now—let me know if you reach desktop or what error/hang you see next. If you're on a corporate/VPN-heavy network, switch to phone hotspot Wi-Fi during boot attempts too. Hang in there!
