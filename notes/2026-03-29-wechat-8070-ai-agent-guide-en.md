---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat 8.0.70 AI Agent Integration Guide
translated: false
type: note
---

You're exactly right—it’s a **grayscale (partial) release**. WeChat **8.0.70** (released around March 21, 2026) is a critical version because it officially introduces the native entry point for AI agents like **OpenClaw**.

Here is the breakdown of the situation and what you should do:

### 1. The "ClawBot" Native Plugin
Tencent has added a hidden menu in this version specifically for OpenClaw. If you have 8.0.70, you should check for the native toggle:
* Go to **Me (我)** > **Settings (设置)** > **General (通用)** > **Plugins (辅助功能)**.
* Look for **ClawBot (龙虾机器人)**.
* If it’s there, enable it. This is the "official" way to link your local OpenClaw gateway without using third-party web-bridge hacks that risk account bans.

### 2. Why the "Upgrade" Pop-up?
Since 8.0.70 is currently in a "Gray Release" (灰度测试), the WeChat server might still push upgrade notifications to "stabilize" the version or move you to the full public build. 
* **If you are on iOS:** 8.0.70 is the stable target. If it keeps asking to upgrade, it might be a minor build patch (e.g., 8.0.70.xx). 
* **If you are on Android:** This version is rolling out slower. If you manually installed an APK, the official store (Play Store/Tencent App Gem) might be trying to "revert" you to the last fully verified public version (like 8.0.69).

### 3. Connection Issues (The "Half-Open" State)
If the plugin is installed on your OpenClaw (the "Lobster" side) but WeChat isn't responding:
* **Version Mismatch:** The OpenClaw WeChat CLI requires the protocol hooks found specifically in 8.0.70. If your WeChat "downgrades" or stays on 8.0.69, the message-sending function will fail.
* **Login Verification:** Even if the plugin shows up, Tencent sometimes restricts the "Agent" features to users in certain regions (Guangzhou and Shenzhen users usually get it first).

---

### What to do next?
1.  **Check for the Plugin:** Look in `Settings > Plugins` for **ClawBot**. If it's missing, the "Upgrade" pop-up is likely trying to give you the version that *actually* has the server-side permission turned on.
2.  **Force Refresh:** Kill the WeChat app completely and restart it while your OpenClaw gateway is running. Sometimes the "ClawBot" entry only appears after the app handshakes with a local gateway on the same Wi-Fi.
3.  **Check Logs:** Run `openclaw logs --channel openclaw-weixin` in your terminal. If you see `[Protocol Error: 403]`, it means your WeChat account hasn't been "whitelisted" for the 8.0.70 AI features yet.

**Would you like me to check if there is a specific configuration command to "force-trigger" the ClawBot menu on your version?**