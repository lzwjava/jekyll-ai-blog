---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Stuck MacOS Proxy Update
translated: false
type: note
---

Yes, Clash (like ClashX, Clash for Windows ported to Mac, or similar tools) often sets system-wide **HTTP**, **HTTPS**, and/or **SOCKS** proxies (usually to 127.0.0.1 on ports like 7890/7891) when you enable "Set as System Proxy". If the app crashes, quits improperly, or has a conflict during macOS update/setup, it can leave those proxies active—causing the software update to hang because Apple's update servers can't be reached properly through the local proxy loop.

Since you're already in **Terminal** (likely from macOS Recovery or single-user mode, given the stuck "Software Update Complete" screen), we can disable all proxy settings via the built-in `networksetup` command. This is the cleanest way to clear them without needing the GUI.

### Step 1: Find Your Network Service Name

Most MacBook Airs use **Wi-Fi** (case-sensitive!). Run this to confirm:

```bash
networksetup -listallnetworkservices
```

- Look for the active one (usually **Wi-Fi** or **Wi-Fi** with a * next to it if it's the primary).
- If it's something else (rare, like "Thunderbolt Ethernet"), use that name instead in the commands below.
- Common name on M2 Air: **Wi-Fi**

### Step 2: Check Current Proxy Settings (Optional but Recommended)

Run these to see what's set (replace "Wi-Fi" if needed):

```bash
networksetup -getwebproxy "Wi-Fi"
networksetup -getsecurewebproxy "Wi-Fi"
networksetup -getsocksfirewallproxy "Wi-Fi"
networksetup -getautoproxyurl "Wi-Fi"
```

- You'll likely see Enabled: Yes and Server: 127.0.0.1 Port: 7890 (or similar) for HTTP/HTTPS/SOCKS.

### Step 3: Disable / Clear All Proxies

Run these one by one (use `sudo` if it asks for a password; in Recovery it often doesn't need it, or use your admin password if prompted):

```bash
networksetup -setwebproxystate "Wi-Fi" off
networksetup -setsecurewebproxystate "Wi-Fi" off
networksetup -setsocksfirewallproxystate "Wi-Fi" off
networksetup -setautoproxystate "Wi-Fi" off
```

- These turn **off** HTTP (Web Proxy), HTTPS (Secure Web Proxy), SOCKS, and Automatic Proxy Configuration (PAC URL).
- To be extra thorough (clears any server/port values completely), you can also run:

```bash
networksetup -setwebproxy "Wi-Fi" "" 0
networksetup -setsecurewebproxy "Wi-Fi" "" 0
networksetup -setsocksfirewallproxy "Wi-Fi" "" 0
```

(Empty server and port 0 effectively clears them.)

### Step 4: Verify They Are Off

Re-run the get commands from Step 2—they should now show **Enabled: No**.

### Step 5: Exit and Retry Boot

- Type `exit` (or `reboot`) to leave Terminal/Recovery.
- Choose to **Restart** from the Recovery menu (or force restart by holding power button if needed).
- Your Mac should now boot without the proxy interference and hopefully proceed past the "Software Update Complete" screen to finish setup or reach the desktop.

### Extra Tips for Clash

- Once you're back in macOS normally, open Clash → turn **off** "Set as System Proxy" (or quit Clash completely) before future updates.
- If you use TUN mode in Clash, it usually doesn't touch system proxies—prefer that over system proxy mode.
- If the hang persists after this, go back to Recovery → Disk Utility → First Aid on your drive again, then try **Reinstall macOS** (non-destructive).

Let me know what the `networksetup -listallnetworkservices` shows or if any command errors out—I can adjust! This fixes the vast majority of proxy-caused update hangs.
