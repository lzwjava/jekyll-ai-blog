---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Optimal EasyMesh Setup Guide
translated: false
type: note
---

Question: Suppose there is a main router (China Telecom's 天翼 gateway using PPPoE account like 020xxx@163.gd), and two sub-routers (both TL-XDR3050 EasyMesh version). I want to get them all working with wired repeater / wireless repeater mode, and also considering DHCP mode to connect upstream.

Answer:

Your setup:
- **Main router** = China Telecom 天翼 gateway (光猫/ONT, often ZTE or similar model, uses PPPoE dial-up with account like 020xxx@163.gd).
- **Sub1 and Sub2** = Two TL-XDR3050 EasyMesh edition routers.
- Goal: Make everything work together for better Wi-Fi coverage (full house, no dead zones), supporting wired or wireless repeating, while avoiding IP conflicts or no-internet issues.

The TL-XDR3050 EasyMesh version supports three main modes:
- **Router mode** (default, with its own DHCP).
- **AP (有线中继) mode** — wired repeater/access point (recommended for stability, zero speed loss on wired backhaul).
- **Wireless repeater / EasyMesh mode** — wireless relay/Mesh (one-key via EasyMesh button, supports multi-hop/cascading).

You can mix modes: e.g., use EasyMesh for wireless extension or classic AP for wired. Since you have two sub-routers and mention "DHCP mode to connect upstream," the safest and best-performing way is to use **EasyMesh wireless** (or hybrid wired+wireless) if wireless is needed, or **AP mode** if you can run cables.

### Recommended Setup: Use EasyMesh (Wireless or Hybrid) – Easiest & Supports Multiple Subs
EasyMesh on XDR3050 allows up to 8 nodes total (main + subs), with multi-hop support (e.g., main → sub1 wireless → sub2 wireless). It handles DHCP automatically (only main dials PPPoE and runs DHCP; subs sync settings and disable their own DHCP).

**Steps**:
1. **Prepare the main 天翼 gateway**:
   - Keep it in **Router mode** (default) — it dials PPPoE with your 020xxx@163.gd account and provides internet + DHCP (usually LAN 192.168.1.1).
   - Do **not** change to bridge mode unless you want the XDR3050 to dial PPPoE (more advanced, can give better performance but riskier if account/VLAN issues arise).
   - Connect nothing yet.

2. **Set one XDR3050 as the "main/extended" router (optional but recommended for better control)**:
   - Factory reset both XDR3050 (press RESET 10+ seconds).
   - Connect one XDR3050 temporarily to a PC (Wi-Fi or LAN cable).
   - Log in: http://tplinkwifi.net or 192.168.0.1.
   - If you want it to handle PPPoE instead of the gateway (for full Wi-Fi 6 speed, less double NAT):
     - Advanced > Internet > Change to PPPoE > Enter your 020xxx@163.gd account/password > Save.
     - But first test if the gateway can be bridged (login to gateway 192.168.1.1 with super admin password from telecom, set WAN to Bridge; search "天翼网关 桥接" for model-specific guide).
   - Most users keep gateway as main dialer to avoid complications.

3. **One-key EasyMesh pairing (for wireless repeating)**:
   - Place sub1 near the gateway (good signal overlap).
   - Power on gateway + sub1 XDR3050.
   - Press the **EasyMesh button** (back panel, labeled "易展", hold 1-3 seconds) on **either** device.
   - Lights flash (searching) → solid/blue/green = paired.
   - Sub1 syncs Wi-Fi name/password from gateway (or you can set unified SSID later).
   - Repeat for sub2: Place sub2 near sub1 (or gateway), press EasyMesh button again — it joins the network (auto chooses best parent node, supports 2+ hops).
   - Result: Seamless roaming, single SSID, main gateway handles DHCP/internet, subs act as extenders without IP conflict.

4. **If you prefer wired repeating (better speed/stability, no multi-hop loss)**:
   - On each XDR3050 (after reset):
     - Log in → Advanced > Operation Mode > Select **AP (有线中继)** → Save & reboot.
     - After reboot, it disables DHCP automatically and becomes a pure access point.
   - Connect: Gateway LAN port → Ethernet cable → XDR3050 **LAN port** (not WAN!).
   - Do the same for sub2 (can chain: Gateway → sub1 LAN-to-LAN → sub2 LAN-to-LAN).
   - Set same Wi-Fi SSID/password as gateway for roaming (or different if you want separation).
   - No IP conflict because only gateway runs DHCP.

5. **Avoiding IP Conflicts & "No Response" Issues**:
   - **Never** leave subs in Router mode when connected — they would run duplicate DHCP and cause conflicts (devices get wrong gateway IP, no internet).
   - In EasyMesh: Auto-handles (subs don't run DHCP).
   - In AP mode: DHCP is disabled.
   - If conflict happens: Disconnect subs → reset them → set to AP/EasyMesh → reconnect.
   - Check IPs: On PC, run `ipconfig` (Windows) — Default Gateway should be only the 天翼 gateway IP (e.g. 192.168.1.1).

**Which to Choose?**
- **Wireless only** → EasyMesh one-key (supports sub1 → sub2 hop, good for no-cable houses).
- **Some wired possible** → Hybrid: Wire sub1 to gateway (faster backhaul), wireless sub2 to sub1.
- **Full wired** → AP mode on both subs (fastest, most stable, no speed halving).

Test step-by-step: Start with one sub, confirm internet on its Wi-Fi, then add the second. Update firmware on all devices from TP-Link China site if pairing fails. If PPPoE issues arise when trying bridge, stick with gateway dialing.

References:

- [https://www.tp-link.com.cn/product_2196.html](https://www.tp-link.com.cn/product_2196.html)
- [https://service.tp-link.com.cn](https://service.tp-link.com.cn) (general TP-Link support for EasyMesh/AP setup)
