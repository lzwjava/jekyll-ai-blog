---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mac Stuck After Update Fixes
translated: false
type: note
---

Your MacBook Air M2 getting stuck on the "Software Update Complete" screen after clicking **Continue** (with no further response, spinning wheel, or progress) is a somewhat commonly reported issue during/after macOS Tahoe (macOS 26) installations or post-update boots, especially on Apple Silicon machines like yours. It often relates to the final setup phase hanging, third-party software conflicts, disk issues, or a glitch in the post-install process.

Don't worry—your data is usually still safe, and this is typically fixable without a full erase. Here's a step-by-step troubleshooting guide based on what works for most users in similar situations:

### 1. Force Restart and Retry

- Press and hold the **power button** (Touch ID button) for about 10 seconds until the Mac fully shuts down (screen goes black, no fans/lights).
- Wait 10–30 seconds, then press the power button once to turn it back on.
- It may boot right back to the same "Software Update Complete" screen—try clicking **Continue** again.
- If it loops or hangs again, repeat the force shutdown 2–3 times. Sometimes it needs a few attempts to "unstick" the post-update setup.

Many users report that after a few force restarts, it proceeds to the desktop or finishes any pending setup.

### 2. Boot into Safe Mode

This loads macOS with minimal extensions/drivers, which often bypasses whatever is causing the hang (e.g., incompatible login items, kernel extensions, or background processes).

For your M2 MacBook Air:

- Shut down the Mac completely (hold power button if needed).
- Press and hold the **power button** until you see the startup options window (shows your boot disk/volume).
- Select your startup disk (usually "Macintosh HD").
- Press and hold the **Shift** key, then click **Continue in Safe Mode**.
- Release Shift once it starts booting.
- Log in if prompted (it may take longer the first time).
- If you reach the desktop in Safe Mode:
  - Let it sit for a few minutes—it may finish any pending update tasks.
  - Restart normally (without Shift) from the Apple menu.
- If it still hangs after Safe Mode boot, proceed to the next steps.

### 3. Reset NVRAM (Non-Volatile RAM)

This clears temporary settings that can interfere with boot/update processes.

- Shut down the Mac.
- Press the power button, then immediately hold **Option + Command + P + R**.
- Hold for about 20 seconds (until you hear the startup chime twice or see the Apple logo appear/disappear twice on M-series Macs).
- Release and let it boot normally.

### 4. Boot into Recovery Mode and Run Disk Utility

If the above doesn't work:

- Shut down.
- Press and hold the **power button** until startup options appear.
- Click **Options** > **Continue** to enter macOS Recovery.
- Select your user/language if prompted.
- From the utilities window:
  - Choose **Disk Utility** > **Continue**.
  - Select your main drive (usually "Apple SSD" or "Macintosh HD" in the sidebar—click **View > Show All Devices** if needed).
  - Click **First Aid** > **Run** (repair the disk and container if errors show).
  - Quit Disk Utility when done.
- Back in Recovery, you can also try **Reinstall macOS** (choose Tahoe if available—it reinstalls the OS without erasing your data/apps).
- If reinstall hangs again, exit and restart normally first.

### Additional Tips

- Make sure you're connected to power (charger plugged in) and a stable Wi-Fi network—some post-update steps require internet to finalize.
- Disconnect any external devices (USB drives, hubs, displays) before trying the above—they can sometimes cause conflicts.
- If you have a recent Time Machine backup (or can access one from another Mac), that's great insurance, but most people don't need to restore from it here.
- If none of this gets you past the screen after several tries (e.g., stuck looping for hours/days), it may need a clean install from Recovery (which erases data—back up first if possible via Target Disk Mode to another Mac) or Apple Support/hardware check.

If you try these and let me know what happens (e.g., does Safe Mode work? Any error messages?), I can narrow it down further. Hang in there—this is frustrating but usually resolvable! If it's still under warranty/AppleCare, contacting Apple Support directly (via chat/phone or Genius Bar) is also a good move—they can run remote diagnostics.
